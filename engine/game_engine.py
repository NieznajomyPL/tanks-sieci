import enum
import pygame
import time
import math

from . import terrains
from . import events
from . import game_objects
from . import states


class GameEngine:
    def __init__(self, width, height):
        self.is_running = False
        
        self.display_width = width
        self.display_height = height
        self.display = pygame.display.set_mode((width, height))
        
        self.game_objects_list = []
        self.tanks = []
        self.tank_index = 0
        
        self.terrain = terrains.Terrain(width, height, seed=4)
        self.terrain.generate_terrain()
        self.terrain.draw_terrain()
        
        self.terrain_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.background_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        self.all_states = {
            "start": states.StartState(self),
            "player_turn": states.PlayerTurnState(self),
            "physic_stablize": states.PhycicStablizeState(self),
            "gameover": states.GameOverState(self)
        }
        self.current_state = self.all_states["start"]
    
        self.mouse_pressed_time = 0
    
        self.tank_control_by_player = None

        self.is_stable = True
        
        self.deltatime = 0
        
        self.event_manager = events.EventManager()
        self.event_manager.create_event("on_right_mouse_bttn_down")
        self.event_manager.get_event("on_right_mouse_bttn_down").register(self.make_boom)
        
        self.event_manager.create_event("on_mid_mouse_bttn_down")
        self.event_manager.get_event("on_mid_mouse_bttn_down").register(self.create_player_tank)
        
        self.event_manager.create_event("on_left_mouse_bttn_down")
        self.event_manager.get_event("on_left_mouse_bttn_down").register(self.shoot_missile)
        
        self.event_manager.create_event("on_mouse_move")
        self.event_manager.get_event("on_mouse_move").register(self.aim_tank)
        
    def change_state(self, new_state):
        self.current_state.exit_state()
        self.current_state = new_state
        self.current_state.enter_state()
    
    def draw(self):
        self.display.fill((255, 255, 255))
        
        self.terrain_surface = self.terrain.get_terrain_surface()
        pygame.draw.circle(self.background_surface, (255, 255, 0), (100, 200), 30)
        
        self.display.blits([(self.terrain_surface, (0, 0)), (self.background_surface, (0, 0))])
        
        for go in self.game_objects_list:
            go.draw(self.display)
        
        pygame.display.flip()
    
    def update(self, deltatime):
        self.current_state.update()
    
    def create_player_tank(self, game_engine, x, y):
        tank = game_objects.Tank(x, y)
        self.game_objects_list.append(tank)
        self.tanks.append(tank)
    
    def aim_tank(self, game_engine, x, y):
        if self.tank_control_by_player is not None:
            self.tank_control_by_player.barrel_angle = math.atan2(y - self.tank_control_by_player.posy, x - self.tank_control_by_player.posx)
    
    def make_boom(self, game_engine, x, y):
        r = 100
        self.terrain.boom(self, x, y, r)
        game_objects.boom(self, x, y, r)
        
    def shoot_missile(self, game_engine, x, y):
        if self.tank_control_by_player is not None or not self.tank_control_by_player.dead:
            self.tank_control_by_player.shoot_power = min(max (2, (time.time() - self.mouse_pressed_time) * 4), 30)
            self.tank_control_by_player.fire(self.game_objects_list)
    
    def enemy_turn(self):
        self.tank_control_by_enemy.barrel_angle = math.pi / 4
        self.tank_control_by_enemy.fire(self.game_objects_list)

    def handle_event(self):
        for event in pygame.event.get():
            self.current_state.handle_input(event)
            
            if event.type == pygame.QUIT:
                self.is_running = False
    
    def game_loop(self):
        pygame.init()
        
        self.is_running = True
        clock = pygame.time.Clock()

        self.create_player_tank(self, 250, 200)
        self.create_player_tank(self, self.display_width-250, 200)
        
        self.tank_control_by_player = self.tanks[self.tank_index]

        while self.is_running:
            t = clock.tick(60)
            self.deltatime = t / 1000
            
            self.handle_event()
            self.update(self.deltatime)
            self.draw()
            
        pygame.quit()



