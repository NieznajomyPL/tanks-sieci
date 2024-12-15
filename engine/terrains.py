import math
import pygame
from perlin_noise import PerlinNoise


class Terrain:
    def __init__(self, width, height, seed=42):
        self.terrain = Terrain.empty_terrain(width, height)
        self.surface = pygame.Surface((width, height))
        self.seed = seed
        self.width = width
        self.height = height

    @staticmethod
    def empty_terrain(width, height):
        return [[0 for _ in range(width)] for _ in range(height)]
    
    def generate_terrain(self):
        noise = PerlinNoise(2, seed=self.seed)
        noise2 = PerlinNoise(8, seed=self.seed)
        t = [[0 for _ in range(self.width)] for _ in range(self.height)]

        heights = [
            noise((col / self.width, 0)) + noise2((col / self.width, 0)) * 0.5 for col in range(self.width)
        ]
        global_valley = abs(min(heights))
        heights = list(map(lambda x: x + global_valley, heights))

        for col in range(self.width):
            h = heights[col] * self.height
            for row in range(self.height):
                if h > row:
                    t[self.height - 1 - row][col] = 1
        
        self.terrain = t

        return self.terrain

    def boom(self, game_engine, x, y, r):
        x = math.floor(x)
        y = math.floor(y)
        for i in range(max(0, y - r), min(len(self.terrain), y + r + 1)):
            for j in range(max(0, x - r), min(len(self.terrain[0]), x + r + 1)):
                if (j - x) ** 2 + (i - y) ** 2 < r * r:
                    self.terrain[i][j] = 0

        pygame.draw.circle(self.surface, pygame.Color(0, 0, 0, 0), (x, y), r)

    def draw_terrain(self):
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((0, 0, 0, 0))
        for row in range(len(self.terrain)):
            for col in range(len(self.terrain[0])):
                if self.terrain[row][col] == 1:
                    self.surface.set_at((col, row), (0, 255, 0))
        return self.surface
    
    def get_terrain_surface(self):
        return self.surface
