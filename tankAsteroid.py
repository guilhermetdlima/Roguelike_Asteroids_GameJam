import pygame
import random

from enemy import Enemy


class TankAsteroid(Enemy):
    
    def __init__(self, screen_width, screen_height, multiplier, money = 2, score = 100, speed=2, health=20, damage=1, color=(60, 60, 60)):
        super().__init__(screen_width, screen_height, speed, health, damage, score, money, multiplier, width=random.randrange(70, 76, 1), height=random.randrange(70, 76, 1), color=color)
        