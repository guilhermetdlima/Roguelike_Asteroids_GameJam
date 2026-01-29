
import pygame
import random

from enemy import Enemy

class StealthAsteroid(Enemy):
    
    def __init__(self, screen_width, screen_height, multiplier, money = 1, score = 400, speed=8, health=15, damage=1):
        super().__init__(screen_width, screen_height, speed, health, damage, score, money, multiplier, width=random.randrange(37, 43, 1), height=random.randrange(37, 43, 1), color=(6, 6, 6))