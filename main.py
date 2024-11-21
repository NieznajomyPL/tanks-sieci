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

def boom(objects, terrain, x, y, r):
    for i, row in enumerate(terrain):
        for j, col in enumerate(row):
            if (j - x) ** 2 + (i - y) ** 2 < r*4:
                terrain[i][j] = 0
            
    for go in objects:
        dx = go.posx - x
        dy = go.posy - y

        dist = math.sqrt(dx*dx + dy*dy)
        dist = 0.001 if dist < 0.001 else dist

        if dist < r:
            go.velox += (dx / dist) * r
            go.veloy += (dy / dist) * r
            go.stable = False

    for n in range(10):
        objects.append(game_objects.Debry(x, y))

def handle_event(game_objects_list, terrain):
    status = [True, False]
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if event.button == 1:
                game_objects_list.append(game_objects.Missile(pos[0], pos[1]))
            if event.button == 3:
                boom(game_objects_list, terrain, pos[0], pos[1], 100)
                status = [True, True]
        if event.type == pygame.QUIT:
            return [False, False]
    return status

def update_physics(game_objects_list, terrain, deltatime):
    for go in game_objects_list:
        go.accy += GRAVITY
        go.velox += go.accx
        go.veloy += go.accy

        potencialx = go.posx + go.velox * deltatime
        potencialy = go.posy + go.veloy * deltatime

        go.accx = 0
        go.accy = 0
        go.stable = False

        veloangle = math.atan2(go.veloy, go.velox)
        go.angle = veloangle
        responsex = 0
        responsey = 0
        collision = False

        x = 16
        for n in range(x+1):
            angle = (n*math.pi/x)+veloangle-math.pi/2

            testposx = go.r * math.cos(angle) + potencialx
            testposy = go.r * math.sin(angle) + potencialy

            testposx = WIDTH - 1 if testposx >= WIDTH else testposx
            testposy = HEIGHT - 1 if testposy >= HEIGHT else testposy

            testposx = 0 if testposx < 0 else testposx
            testposy = 0 if testposy < 0 else testposy

            if terrain[int(testposy)][int(testposx)] != 0:
                responsex += potencialx - testposx
                responsey += potencialy - testposy
                collision = True
        
        magvelo = math.sqrt(go.velox*go.velox + go.veloy*go.veloy)
        magresponse = math.sqrt(responsex*responsex+responsey*responsey)
        if magresponse < 0.005:
            magresponse = 0.005

        if collision:
            go.stable = True

            dot = go.velox * (responsex/magresponse) + go.veloy * (responsey/magresponse)
            go.velox = go.fricion * (-2 * dot * (responsex/magresponse) + go.velox)
            go.veloy = go.fricion * (-2 * dot * (responsey/magresponse) + go.veloy)

            if go.bounce_before > 0:
                go.bounce_before -= 1
            go.dead = go.bounce_before == 0
        else:
            go.posx = potencialx
            go.posy = potencialy
        
        if magvelo < 0.05: 
            go.stable = True

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))

def main():
    terrain = terrains.generate_level(WIDTH, HEIGHT, terrain_seed=100)

    terrain_surface = draw_terrain(terrain)

    clock = pygame.time.Clock()
    run = True

    game_objects_list = []

    while run:
        t = clock.tick(60)
        deltatime = t / 1000

        run, is_update_terrain = handle_event(game_objects_list, terrain)
        if is_update_terrain:
            terrain_surface = draw_terrain(terrain)

        win.fill((255, 255, 255))
        win.blit(terrain_surface, (0,0))
        # Słoneczko :-)
        pygame.draw.circle(terrain_surface, (255, 255, 0), (100, 200), 30)

        update_physics(game_objects_list, terrain, deltatime)

        for i, _ in enumerate(game_objects_list):
            if game_objects_list[i].dead:
                del game_objects_list[i]

        for go in game_objects_list:
            go.draw(win)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()



