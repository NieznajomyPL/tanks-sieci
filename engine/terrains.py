import math
from perlin_noise import PerlinNoise


def generate_level(width, height, terrain_seed=42):
    noise = PerlinNoise(2, seed=terrain_seed)
    noise2 = PerlinNoise(8, seed=terrain_seed)
    level = [[0 for _ in range(width)] for _ in range(height)]

    heights = [
        noise((col / width, 0)) + noise2((col / width, 0)) * 0.5 for col in range(width)
    ]
    global_valley = abs(min(heights))
    heights = list(map(lambda x: x + global_valley, heights))

    for col in range(width):
        h = heights[col] * height
        for row in range(height):
            if h > row:
                level[height - 1 - row][col] = 1

    return level
