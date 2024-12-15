import enum
import pygame
import time
import math

from . import terrains
from . import events
from . import game_objects

class MenuState(enum.Enum):
    IN_GAME = 0,
    IN_MENU = 1
    

class GameEngine:
    def __init__(self, width, height):
        self.is_running = False
        
        self.display_width = width
        self.display_height = height
        self.display = pygame.display.set_mode((width, height))
        
        self.game_objects_list = []
        self.terrain = terrains.Terrain(width, height)
        self.terrain.generate_terrain()
        self.terrain.draw_terrain()
        
        self.terrain_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.background_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        self.menu_state = MenuState.IN_GAME
    
        self.mouse_pressed_time = 0
    
        self.tank_control_by_player = None
        
        self.event_manager = events.EventManager()
        self.event_manager.create_event("on_right_mouse_bttn_down")
        self.event_manager.get_event("on_right_mouse_bttn_down").register(self.make_boom)
        
        self.event_manager.create_event("on_mid_mouse_bttn_down")
        self.event_manager.get_event("on_mid_mouse_bttn_down").register(self.create_player_tank)
        
        self.event_manager.create_event("on_left_mouse_bttn_down")
        self.event_manager.get_event("on_left_mouse_bttn_down").register(self.shoot_missile)
        
        self.event_manager.create_event("on_mouse_move")
        self.event_manager.get_event("on_mouse_move").register(self.aim_tank)
    
    
    def draw(self):
        self.display.fill((255, 255, 255))
        
        self.terrain_surface = self.terrain.get_terrain_surface()
        pygame.draw.circle(self.background_surface, (255, 255, 0), (100, 200), 30)
        
        self.display.blits([(self.terrain_surface, (0, 0)), (self.background_surface, (0, 0))])
        
        for go in self.game_objects_list:
            go.draw(self.display)
        
        pygame.display.flip()
    
    def update(self, deltatime):
        for go in self.game_objects_list:
            go.update_physics(self.terrain.terrain, deltatime)
        
        for i, _ in enumerate(self.game_objects_list):
            if self.game_objects_list[i].dead:
                self.game_objects_list[i].after_death(self)
                del self.game_objects_list[i]
    
    def create_player_tank(self, game_engine, x, y):
        self.tank_control_by_player = game_objects.Tank(x, y)
        self.game_objects_list.append(self.tank_control_by_player)
    
    def aim_tank(self, game_engine, x, y):
        if self.tank_control_by_player is not None:
            self.tank_control_by_player.barrel_angle = math.atan2(y - self.tank_control_by_player.posy, x - self.tank_control_by_player.posx)
    
    def make_boom(self, game_engine, x, y):
        r = 100
        self.terrain.boom(self, x, y, r)
        game_objects.boom(self, x, y, r)
        
    def shoot_missile(self, game_engine, x, y):
        if self.tank_control_by_player is not None:
            self.tank_control_by_player.power = max (2, (time.time() - self.mouse_pressed_time) * 4)
            self.tank_control_by_player.fire(self.game_objects_list)
    
    def handle_event(self):
        pos = pygame.mouse.get_pos()
        self.event_manager.get_event("on_mouse_move").trigger(self, pos[0], pos[1])
        
        for event in pygame.event.get():
            if self.menu_state == MenuState.IN_GAME:
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.event_manager.get_event("on_left_mouse_bttn_down").trigger(self, pos[0], pos[1])
                        self.mouse_pressed_time = 0
                    if event.button == 2:
                        self.event_manager.get_event("on_mid_mouse_bttn_down").trigger(self, pos[0], pos[1])
                    if event.button == 3:
                        self.event_manager.get_event("on_right_mouse_bttn_down").trigger(self, pos[0], pos[1])
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.mouse_pressed_time = time.time()
            if self.menu_state == MenuState.IN_MENU:
                pass
            if event.type == pygame.QUIT:
                self.is_running = False
    
    def game_loop(self):
        pygame.init()
        
        self.is_running = True
        clock = pygame.time.Clock()

        while self.is_running:
            t = clock.tick(60)
            deltatime = t / 1000
            
            self.handle_event()
            self.update(deltatime)
            self.draw()
            
        pygame.quit()


