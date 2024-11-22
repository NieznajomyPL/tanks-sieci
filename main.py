import pygame
import math
import random

from engine import game_objects
from engine import terrains


WIDTH, HEIGHT = 800, 600
GRAVITY = 20


def draw_terrain(terrain):
    terrain_surface = pygame.Surface((WIDTH, HEIGHT))
    terrain_surface.fill((0, 0, 0, 0))
    for row in range(len(terrain)):
        for col in range(len(terrain[0])):
            if terrain[row][col] == 1:
                terrain_surface.set_at((col, row), (0, 255, 0))
    return terrain_surface



def handle_event(game_objects_list, terrain):
    global run, is_update_terrain
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if event.button == 1:
                game_objects_list.append(game_objects.Missile(pos[0], pos[1]))
            if event.button == 2:
                game_objects_list.append(game_objects.GameObject(pos[0], pos[1]))
            if event.button == 3:
                game_objects.boom(game_objects_list, terrain, pos[0], pos[1], 100)
                is_update_terrain = True
        if event.type == pygame.QUIT:
            run = False


pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
is_update_terrain = False
run = True

def main():
    global is_update_terrain
    terrain = terrains.generate_level(WIDTH, HEIGHT, terrain_seed=100)

    terrain_surface = draw_terrain(terrain)

    clock = pygame.time.Clock()

    game_objects_list = []

    while run:
        t = clock.tick(60)
        deltatime = t / 1000

        handle_event(game_objects_list, terrain)
        
        if is_update_terrain:
            is_update_terrain = False
            terrain_surface = draw_terrain(terrain)

        win.fill((255, 255, 255))
        win.blit(terrain_surface, (0, 0))
        # Słoneczko :-)
        pygame.draw.circle(terrain_surface, (255, 255, 0), (100, 200), 30)

        for go in game_objects_list:
            go.update_physics(terrain, deltatime)

        for i, _ in enumerate(game_objects_list):
            if game_objects_list[i].dead:
                game_objects_list[i].after_death(game_objects_list, terrain)
                is_update_terrain = True
                del game_objects_list[i]

        for go in game_objects_list:
            go.draw(win)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
