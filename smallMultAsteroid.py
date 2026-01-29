import pygame

from enemy import Enemy

class SmallMultAsteroid(Enemy):

    def __init__(self, screen_width, screen_height, multiplier, money = 1, score = 100, speed=6, health=2, damage=1, width=30, height=30, color=(20, 120, 40), posX=None, posY=None):
        super().__init__(screen_width, screen_height, speed, health, damage, score, money, multiplier, width,  height, color, posX, posY)

