import pygame
import random

from enemy import Enemy


class BaseAsteroid(Enemy):
    
    def __init__(self, screen_width, screen_height, multiplier, money = 1, score = 50, speed=2, health=10, damage=1):
        super().__init__(screen_width, screen_height, speed, health, damage, score, money, multiplier, width=random.randrange(45, 50, 1), height=random.randrange(45, 50, 1), color=(93, 93, 93))
    