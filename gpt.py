import pygame
import math
import random
from perlin_noise import PerlinNoise

import matplotlib.pyplot as plt



# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu gry
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gra Artyleryjska - Czołgi")

def generate_level():
    noise = PerlinNoise(3)
    terrain = [noise([i/HEIGHT]) for i in range(HEIGHT)]
    global_valley = abs(min(terrain))
    terrain = list(map(lambda x: x+global_valley, terrain))
    level_map = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for i, t in enumerate(terrain):
        h = math.ceil(t*HEIGHT)
        for k in range(HEIGHT):
            for j in range(WIDTH):
                if j <= h:
                    level_map[k][j] = 1
        # level_map[]
    # # print(terrain)
    # plt.plot(range(HEIGHT), terrain)
    # plt.show()
    return level_map

level_map = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
level_map = generate_level()

# Kolory
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Ustawienia gry
TANK_WIDTH, TANK_HEIGHT = 40, 20
GRAVITY = 0.5
ANGLE_STEP = 1
POWER_STEP = 1

# Klasa czołgu
class Tank:
    def __init__(self, x, color):
        self.x = x
        self.y = HEIGHT - TANK_HEIGHT - 10
        self.color = color
        self.angle = 45  # Kąt początkowy
        self.power = 20  # Siła początkowa

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, TANK_WIDTH, TANK_HEIGHT))
        end_x = self.x + TANK_WIDTH / 2 + 30 * math.cos(math.radians(self.angle))
        end_y = self.y - 30 * math.sin(math.radians(self.angle))
        pygame.draw.line(win, self.color, (self.x + TANK_WIDTH / 2, self.y), (end_x, end_y), 3)

    def adjust_angle(self, delta):
        self.angle = max(0, min(90, self.angle + delta))

    def adjust_power(self, delta):
        self.power = max(5, min(50, self.power + delta))

# Klasa pocisku
class Bullet:
    def __init__(self, x, y, angle, power):
        self.x = x
        self.y = y
        self.angle = angle
        self.power = power
        self.vx = power * math.cos(math.radians(angle))
        self.vy = -power * math.sin(math.radians(angle))

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += GRAVITY  # Grawitacja wpływa na prędkość pionową

    def draw(self, win):
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), 5)

    def off_screen(self):
        return self.x < 0 or self.x > WIDTH or self.y > HEIGHT

# Funkcja sprawdzająca trafienie
def check_collision(bullet, tank):
    return tank.x <= bullet.x <= tank.x + TANK_WIDTH and tank.y <= bullet.y <= tank.y + TANK_HEIGHT

def draw():
    pass



# Funkcja główna
def main():
    clock = pygame.time.Clock()
    run = True

    # Gracze
    player_tank = Tank(100, GREEN)
    enemy_tank = Tank(WIDTH - 150, BLACK)

    bullets = []
    enemy_turn = False

    terrain_surface = pygame.Surface((WIDTH, HEIGHT))
    terrain_surface.fill((255,255,255,128))
    for k in range(HEIGHT):
        for j in range(WIDTH):
            terrain_surface.set_at((k, j),(0, 255*level_map[k][j], 0))

    while run:
        clock.tick(30)
        win.fill(WHITE)
    

        
        win.blit(terrain_surface, (0, 0))

        # Obsługa wyjścia
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Rysowanie czołgów
        player_tank.draw(win)
        enemy_tank.draw(win)

        # Rysowanie i ruch pocisków
        for bullet in bullets[:]:
            bullet.move()
            bullet.draw(win)
            if bullet.off_screen():
                bullets.remove(bullet)
            elif check_collision(bullet, enemy_tank if not enemy_turn else player_tank):
                print("Trafienie!" if not enemy_turn else "Zostałeś trafiony!")
                bullets.remove(bullet)
                enemy_turn = not enemy_turn

        # Sterowanie czołgiem gracza
        keys = pygame.key.get_pressed()
        if not enemy_turn:
            if keys[pygame.K_LEFT]:
                player_tank.adjust_angle(-ANGLE_STEP)
            if keys[pygame.K_RIGHT]:
                player_tank.adjust_angle(ANGLE_STEP)
            if keys[pygame.K_UP]:
                player_tank.adjust_power(POWER_STEP)
            if keys[pygame.K_DOWN]:
                player_tank.adjust_power(-POWER_STEP)
            if keys[pygame.K_SPACE]:
                # Strzał
                bullet_x = player_tank.x + TANK_WIDTH / 2
                bullet_y = player_tank.y
                bullets.append(Bullet(bullet_x, bullet_y, player_tank.angle, player_tank.power))
                enemy_turn = True  # Przejście tury na przeciwnika

        # Ruch przeciwnika
        if enemy_turn and len(bullets) == 0:
            enemy_angle = random.randint(30, 60)
            enemy_power = random.randint(15, 25)
            bullet_x = enemy_tank.x + TANK_WIDTH / 2
            bullet_y = enemy_tank.y
            bullets.append(Bullet(bullet_x, bullet_y, enemy_angle, enemy_power))
            enemy_turn = False  # Przejście tury na gracza

        # Wyświetlanie danych
        font = pygame.font.SysFont(None, 24)
        angle_text = font.render(f"Kąt: {player_tank.angle}", True, BLACK)
        power_text = font.render(f"Moc: {player_tank.power}", True, BLACK)
        win.blit(angle_text, (10, 10))
        win.blit(power_text, (10, 30))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
