import pygame
import math
import random
import time

from engine import game_engine
from engine import game_objects


WIDTH, HEIGHT = 800, 600
GRAVITY = 20

def main():
    ge = game_engine.GameEngine(WIDTH, HEIGHT)
    ge.game_loop()


if __name__ == "__main__":
    main()
