import pygame
import time

class GameState:
    def __init__(self, game):
        self.game = game

    def enter_state(self):
        pass

    def exit_state(self):
        pass

    def update(self):
        pass

    def handle_input(self, input_data):
        pass


class StartState(GameState):
    def enter_state(self):
        print("Game Starting! Prepare for battle.")

    def update(self):
        print("Transitioning to Player Turn State.")
        self.game.change_state(self.game.all_states["physic_stablize"])


class PhycicStablizeState(GameState):
    def __init__(self, game):
        super().__init__(game)
    
    def update(self):
        self.game.is_stable = True
        for go in self.game.game_objects_list:
            go.update_physics(self.game.terrain.terrain, self.game.deltatime)
            self.game.is_stable = self.game.is_stable and go.stable
        
        for i, _ in enumerate(self.game.game_objects_list):
            if self.game.game_objects_list[i].dead:
                self.game.is_stable = False
                self.game.game_objects_list[i].after_death(self.game)
                del self.game.game_objects_list[i]
        
        if self.game.is_stable:
            self.game.change_state(self.game.all_states["player_turn"])

class PlayerTurnState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.current_player = 0

    def enter_state(self):
        self.game.tank_index = (self.game.tank_index + 1) % len(self.game.tanks)
        self.game.tank_control_by_player = self.game.tanks[self.game.tank_index]
        print(f"Player {self.game.tank_index}'s turn.")

    def handle_input(self, event):
        pos = pygame.mouse.get_pos()
        self.game.event_manager.get_event("on_mouse_move").trigger(self.game, pos[0], pos[1])
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.game.event_manager.get_event("on_left_mouse_bttn_down").trigger(self.game, pos[0], pos[1])
                self.game.mouse_pressed_time = 0
                self.game.change_state(self.game.all_states["physic_stablize"])
            if event.button == 2:
                self.game.event_manager.get_event("on_mid_mouse_bttn_down").trigger(self.game, pos[0], pos[1])
            if event.button == 3:
                self.game.event_manager.get_event("on_right_mouse_bttn_down").trigger(self.game, pos[0], pos[1])
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.game.mouse_pressed_time = time.time()

    def update(self):
        pass


class GameOverState(GameState):
    def enter_state(self):
        print("Game Over!")
    def update(self):
        my_font = pygame.font.SysFont('Noto sans', 30)
        text_surface = my_font.render('GAME END', False, (255, 255, 255))
        self.game.background_surface.blit(text_surface, (0,0))