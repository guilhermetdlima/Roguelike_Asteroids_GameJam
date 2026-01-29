import pygame
import random

from enemy import Enemy
from smallMultAsteroid import SmallMultAsteroid

class BossAsteroid1(Enemy):
    
    def __init__(self, screen_width, screen_height, multiplier, money = 15, score = 10000, speed=2, health=120, damage=5, color=(70, 70, 70)):
        super().__init__(screen_width, screen_height, speed, health, damage, score, money, multiplier, width=300, height=300, color=color)


    def on_death(self, bullets, bullet_config):
        # Spawn 4 SmallMultAsteroids at the center of the MultAsteroid
        small_asteroids = []
        for _ in range(8):
            small_asteroid = SmallMultAsteroid(
                self.rect.centerx,  # Use the center x-coordinate of the parent asteroid
                self.rect.centery,  # Use the center y-coordinate of the parent asteroid
                money=self.money,
                score=500,
                multiplier= self.multiplier,
                speed=5,
                health=20,
                damage=1,
                width=random.randrange(70, 76, 1),
                height=random.randrange(70, 76, 1),
                color=(60, 60, 60),
                posX=self.x,
                posY = self.y
            )
            small_asteroids.append(small_asteroid)
        return small_asteroids