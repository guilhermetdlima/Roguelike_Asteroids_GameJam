import pygame
import math
import random
from bulletConfig import BulletConfig
from bullet import Bullet
from player import Player

class Enemy:
    def __init__(self, screen_width, screen_height, speed, health, damage, score, money, multiplier = 1, width=50, height=50, color=(255, 0, 0), posX=None, posY=None):
        self.multiplier = multiplier
        self.width = width
        self.height = height
        self.speed = speed + multiplier * 0.5 if speed > 0 else 0
        self.health = (health * multiplier)
        self.damage = damage
        self.color = color
        self.score = score
        self.money = money
        self.original_color = color  
        self.hit_timer = 0  

        if posX is not None and posY is not None:
            # Spawn at the specified location
            self.x = posX
            self.y = posY

            # Move in a random direction
            self.angle = random.uniform(0, 2 * math.pi)

        else:
            # Spawn from a screen edge
            side = random.choice(["top", "bottom", "left", "right"])
            if side == "top":
                self.x = random.randrange(0, screen_width)
                self.y = 0
            elif side == "bottom":
                self.x = random.randrange(0, screen_width)
                self.y = screen_height
            elif side == "left":
                self.x = 0
                self.y = random.randrange(0, screen_height)
            else:  
                self.x = screen_width
                self.y = random.randrange(0, screen_height)

            # Move toward the center-ish
            center_x = (screen_width / 2) + random.randint(-150, 150)
            center_y = (screen_height / 2) + random.randint(-150, 150)
            dx = center_x - self.x
            dy = center_y - self.y
            self.angle = math.atan2(dy, dx)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def move(self, screen_width, screen_height):
        # Update the asteroid's position
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        # Wrap around the screen horizontally
        if self.x + self.width < 0:  # Off the left side
            self.x = screen_width
        elif self.x > screen_width:  # Off the right side
            self.x = -self.width

        # Wrap around the screen vertically
        if self.y + self.height < 0:  # Off the top
            self.y = screen_height
        elif self.y > screen_height:  # Off the bottom
            self.y = -self.height

        # Update the rect to match the new position
        self.rect.topleft = (self.x, self.y)

        return False  # No need to signal removal

    def draw(self, screen):
        if self.hit_timer > 0:
            self.hit_timer -= pygame.time.get_ticks() / 60  
            pygame.draw.rect(screen, (255, 0, 0), self.rect)  
        else:
            pygame.draw.rect(screen, self.original_color, self.rect)  

    def take_damage(self, amount, bullets, bullet_config):
        self.health -= amount
        self.hit_timer = 200  
        if self.health <= 0:
            return self.on_death(bullets, bullet_config)
        return False

    def on_death(self, bullets, bullet_config):
        #print("Enemy destroyed")
        if bullet_config.bomb:
            num_bullets = 4
            angle_step = 360 / num_bullets
            bullet_config_Kaboon = BulletConfig(speed=bullet_config.speed, damage=bullet_config.damage, size=bullet_config.size, homing=False)  # ajuste conforme necessário

            for i in range(num_bullets):
                angle = i * angle_step
                bullet = Bullet(self.x, self.y, angle, bullet_config_Kaboon)
                bullets.append(bullet)
        return True



