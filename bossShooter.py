import pygame
import math
import os
from enemy import Enemy
from bullet import Bullet  
from bulletConfig import BulletConfig



class BossShooter(Enemy):

    def __init__(self, screen_width, screen_height, player, multiplier, bullet_config, sprite, bulletSprite, money=100, score=5000, speed=0, health=500, damage=5):
        self.max_health = health
        self.screen_width = screen_width
        self.screen_height = screen_height
        width, height = 500, 500
        deslocamento_x = 120
        deslocamento_y = 85
        self.bulletSprite = bulletSprite
        x = screen_width - width - 20 + deslocamento_x
        y = screen_height // 2 - height // 2 + deslocamento_y

        super().__init__(screen_width, screen_height, speed, health, damage, score, money, multiplier,
                         width=width, height=height, color=(255, 0, 0))  # vermelho para destacar

        self.x = x
        self.y = y
        hitbox_margin = 40  # pixels de margem
        self.rect = pygame.Rect(self.x + hitbox_margin, self.y + hitbox_margin, width - 2*hitbox_margin, height - 2*hitbox_margin)
        self.sprite = sprite
        
        self.player = player
        self.bullet_config = BulletConfig(damage=1, speed=15)
        self.last_shot_time = 0
        self.shoot_cooldown = 1000  # ms entre tiros


    def update(self, enemy_bullets):
        velocidade_vertical = 2  # ajuste a velocidade como quiser
        deslocamento_frente = 0.5  # velocidade para frente (direita)

        # Exemplo: faz o boss "quicar" entre topo e base da tela
        if not hasattr(self, "moving_down"):
            self.moving_down = True

        if not hasattr(self, "moving_front"):
            self.moving_front = True

        if self.moving_down:
            self.y += velocidade_vertical
            if self.y + self.height >= 0.95 * self.screen_height:  # Limite inferior MAIS BAIXO (de 0.9 para 0.95)
                self.y = 0.95 * self.screen_height - self.height
                self.moving_down = False
        else:
            self.y -= velocidade_vertical
            if self.y <= 0.2 * self.screen_height:  # Limite superior MAIS ALTO (de 0.1 para 0.2)
                self.y = 0.2 * self.screen_height
                self.moving_down = True

            limite_esquerda = self.screen_width - self.width - 40  # Mais à direita
            limite_direita = self.screen_width - self.width + 100   # Pouco à esquerda

            if self.moving_front:
                self.x += deslocamento_frente
                if self.x >= limite_direita:
                    self.x = limite_direita
                    self.moving_front = False
            else:
                self.x -= deslocamento_frente
                if self.x <= limite_esquerda:
                    self.x = limite_esquerda
                    self.moving_front = True

        

        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            px = self.player.x + self.player.width // 2
            py = self.player.y + self.player.height // 2
            cx = self.x 
            cy = self.y + self.height // 2
            angle = math.degrees(math.atan2(py - cy, px - cx))
            print("Boss atirou!")
            print(f"Bullet criada em ({cx}, {cy}) com ângulo {angle}")
            if self.health > self.max_health / 2:
                bullet = Bullet(cx, cy, angle, self.bullet_config, spritesheet=self.bulletSprite)
                bullet.color = (255, 0, 0)
                bullet.size = 20
                bullet.speed = 10
                enemy_bullets.append(bullet)
            elif self.health < self.max_health / 2:
                for cy in [self.y + self.height // 2, self.y + 55, self.y + 440]:
                    bullet = Bullet(cx, cy, angle, self.bullet_config, spritesheet=self.bulletSprite)
                    bullet.color = (255, 0, 255)
                    bullet.size = 35
                    bullet.speed = 20
                    enemy_bullets.append(bullet)

        
            
            self.last_shot_time = current_time

    def draw(self, screen):
        rotated_sprite = pygame.transform.rotate(self.sprite, 90)
        rect = rotated_sprite.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        
        screen.blit(rotated_sprite, rect.topleft)
