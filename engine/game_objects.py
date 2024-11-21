import pygame
import math
import random

class GameObject:
    def __init__(self, x, y):
        self.r = 15
        self.posx = x
        self.posy = y
        self.velox = 0.0
        self.veloy = 0.0
        self.accx = 0.0
        self.accy = 0.0
        self.stable = True
        self.angle = 0
        self.fricion = 0.8

        self.bounce_before = -1
        self.dead = False

    def draw(self, win):
        pygame.draw.circle(win, (255, 0, 0), (self.posx, self.posy), self.r)
        pygame.draw.line(win, (255, 255, 255), (self.posx, self.posy), (self.posx + self.r * math.cos(self.angle), self.posy + self.r * math.sin(self.angle)))

class Debry(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.r = 4
        self.fricion = 0.6
        self.bounce_before = 5

        angle = random.uniform(0, math.pi*2)
        self.velox = math.cos(angle) * random.uniform(80, 150)
        self.veloy = math.sin(angle) * random.uniform(80, 150)

    def draw(self, win):
        pygame.draw.circle(win, (0, 255, 0), (self.posx, self.posy), self.r)

class Missile(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.r = 7
        self.fricion = 0.6
        self.bounce_before = 0

    def draw(self, win):
        # pygame.draw.line(win, (255, 255, 255), (self.posx, self.posy), (self.posx + self.r * math.cos(self.angle), self.posy + self.r * math.sin(self.angle)), width=3)
        pygame.draw.polygon(win, (255, 0, 0), ((self.posx, self.posy), 
            (self.posx - 2 * self.r * math.cos(self.angle + math.pi/8), self.posy - 2 * self.r * math.sin(self.angle + math.pi/8)), 
            (self.posx - 2 * self.r * math.cos(self.angle - math.pi/8), self.posy - 2 * self.r * math.sin(self.angle - math.pi/8))))