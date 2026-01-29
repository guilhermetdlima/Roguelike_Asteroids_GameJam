import pygame
import random

from enemy import Enemy

class FastAsteroid(Enemy):
    
    def __init__(self, screen_width, screen_height, multiplier, money = 1, score = 30, speed=6, health=5, damage=1):
        super().__init__(screen_width, screen_height, speed, health, damage, score, money, multiplier, width=random.randrange(37, 43, 1), height=random.randrange(37, 43, 1), color=(15, 15, 125))