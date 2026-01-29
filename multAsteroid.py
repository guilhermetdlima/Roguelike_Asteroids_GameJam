import pygame
import random

from smallMultAsteroid import SmallMultAsteroid
from enemy import Enemy

class MultAsteroid(Enemy):

    def __init__(self, screen_width, screen_height, multiplier, money = 1, score = 100, speed=3, health=10, damage=1, color=(20, 160, 40)):
        super().__init__(screen_width, screen_height, speed, health, damage, score, money, multiplier, width=random.randrange(57, 63, 1), height=random.randrange(57, 63, 1), color=color)

    def on_death(self, bullets, bullet_config):
        # Spawn 4 SmallMultAsteroids at the center of the MultAsteroid
        small_asteroids = []
        for _ in range(4):
            small_asteroid = SmallMultAsteroid(
                self.rect.centerx,  # Use the center x-coordinate of the parent asteroid
                self.rect.centery,  # Use the center y-coordinate of the parent asteroid
                money=self.money,
                score=self.score,
                multiplier= self.multiplier,
                speed=6,
                health=2,
                damage=1,
                width=random.randrange(20, 30, 1),
                height=random.randrange(20, 30, 1),
                color=(20, 120, 40),
                posX=self.x,
                posY = self.y
            )
            small_asteroids.append(small_asteroid)
        return small_asteroids