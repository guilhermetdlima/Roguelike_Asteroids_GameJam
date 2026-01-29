import pygame
import random

from enemy import Enemy


class SuperTankAsteroid(Enemy):
    
    def __init__(self, screen_width, screen_height, multiplier, money = 2, score = 100, speed=0.5, health=80, damage=1, color=(40, 40, 40)):
        super().__init__(screen_width, screen_height, speed, health, damage, score, money, multiplier, width=random.randrange(90, 95, 1), height=random.randrange(90, 95, 1), color=color)
        