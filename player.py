import pygame
import math
import os
import random

from bulletConfig import BulletConfig
from bullet import Bullet
from laser import LaserBullet



class Player:

    def __init__(self, speed, health, bullet_config: BulletConfig, sprite=None, bulletSprite=None, shootSFX=None):
        self.rotation_angle = 0
        self.rotation_speed = 5
        self.max_health = health 
        self.pending_bullets = []
        self.max_speed = 4
        self.base_max_speed = self.max_speed
        self.width = 50
        self.height = 50
        self.x = 800 // 2 - self.width // 2
        self.y = 600 // 2 - self.height // 2
        is_firing = False
        self.laser_bullet = None
        self.bulletSprite = bulletSprite
        self.bullet_config = bullet_config
        self.last_shot_time = 0
        self.shootSFX = shootSFX
        self.money = 0
        self.score = 0
        self.speed = speed
        self.health = health
        self.color = (0, 0, 255)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.invulnerable_timer = 0  # Timer for invulnerability

        # Atributos de aceleração e velocidade
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 0.2  # Aceleração ao pressionar uma tecla
        self.deceleration = 0.1  # Desaceleração ao soltar a tecla
        self.max_speed = 4  # Velocidade máxima

        self.sprite = sprite

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)

    def move(self, keys, screen_width, screen_height):
        # Aceleração ao pressionar teclas
        if keys[pygame.K_a]:
            self.velocity_x -= self.acceleration
        elif keys[pygame.K_d]:
            self.velocity_x += self.acceleration
        else:
            # Desaceleração horizontal
            if self.velocity_x > 0:
                self.velocity_x -= self.deceleration
                if self.velocity_x < 0:
                    self.velocity_x = 0
            elif self.velocity_x < 0:
                self.velocity_x += self.deceleration
                if self.velocity_x > 0:
                    self.velocity_x = 0

        if keys[pygame.K_w]:
            self.velocity_y -= self.acceleration
        elif keys[pygame.K_s]:
            self.velocity_y += self.acceleration
        else:
            # Desaceleração vertical
            if self.velocity_y > 0:
                self.velocity_y -= self.deceleration
                if self.velocity_y < 0:
                    self.velocity_y = 0
            elif self.velocity_y < 0:
                self.velocity_y += self.deceleration
                if self.velocity_y > 0:
                    self.velocity_y = 0

        # Limitar a velocidade máxima
        self.velocity_x = max(-self.max_speed, min(self.velocity_x, self.max_speed))
        self.velocity_y = max(-self.max_speed, min(self.velocity_y, self.max_speed))

        # Atualizar a posição do jogador
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Impedir que o jogador saia da tela
        if self.x < 0:
            self.x = 0
            self.velocity_x = 0
        if self.x > screen_width - self.width:
            self.x = screen_width - self.width
            self.velocity_x = 0
        if self.y < 0:
            self.y = 0
            self.velocity_y = 0
        if self.y > screen_height - self.height:
            self.y = screen_height - self.height
            self.velocity_y = 0

        # Atualizar o rect do jogador
        self.rect.topleft = (self.x, self.y)

    def add_money(self, amount):
        self.money += amount

    def add_score(self, amount):
        self.score += amount

    def agenda_shoot(self):
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.bullet_config.cooldown * 1000:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            base_angle = math.atan2(mouse_y - (self.y + self.height // 2), mouse_x - (self.x + self.width // 2))
            
            lateral_offset = 0  # distância lateral entre grupos
            angle_between = 10   # graus entre as balas do mesmo grupo
            delay_between_bullets = 100  # ms de delay entre balas da sequência

            # total de grupos laterais
            numB = self.bullet_config.numB  
            # quantidade de balas em cada grupo (multi-tiros)
            multB = self.bullet_config.multB  

           

            for j in range(multB):  # multB = quantos multi-tiros (em sequência, com delay)
                # deslocamento lateral para cada tiro (só se quiser espalhar os pontos de origem)
                dx = math.cos(base_angle + math.pi / 2) * lateral_offset * (j - multB // 2)
                dy = math.sin(base_angle + math.pi / 2) * lateral_offset * (j - multB // 2)

                # cálculo dos ângulos de dispersão para as numB balas
                if numB == 1:
                    angles = [base_angle]
                else:
                    angle_between = 10  # graus entre cada bala
                    spread_deg = angle_between * (numB - 1)
                    spread_rad = math.radians(spread_deg)
                    step = spread_rad / (numB - 1)
                    start_angle = base_angle - spread_rad / 2
                    angles = [start_angle + i * step for i in range(numB)]

                for i, angle in enumerate(angles):
                    scheduled_time = current_time + j * delay_between_bullets  # delay por multitiro, não por ângulo
                    self.pending_bullets.append({
                        "x": self.x + self.width // 2 + dx,
                        "y": self.y + self.height // 2 + dy,
                        "angle": math.degrees(angle),
                        "scheduled_time": scheduled_time,
                        "config": self.bullet_config
                    })

            self.last_shot_time = current_time


    def update_shooting(self, bullets):
        current_time = pygame.time.get_ticks()
        to_shoot = [b for b in self.pending_bullets if b["scheduled_time"] <= current_time]

        for b in to_shoot:
            bullet = Bullet(b["x"], b["y"], b["angle"], b["config"], spritesheet=self.bulletSprite)
            # Crítico: chance baseada em bullet_config.critC
            if random.random() < self.bullet_config.critC:
                bullet.damage *= 2
                bullet.isCrit = 1
            else:
                bullet.isCrit = 0
            bullets.append(bullet)
            if self.shootSFX:
                if self.bullet_config.cooldown < 0.3:
                    self.shootSFX.set_volume(0.1)
                self.shootSFX.play()
            self.pending_bullets.remove(b)

    def shot_laser(self):
        current_time = pygame.time.get_ticks()
        laser_cooldown = 3000  # ms
        if not hasattr(self, "last_laser_time"):
            self.last_laser_time = 0

        if current_time - self.last_laser_time > laser_cooldown:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle = math.degrees(math.atan2(mouse_y - (self.y + self.height // 2), mouse_x - (self.x + self.width // 2)))
            self.last_laser_time = current_time
            self.laser_bullet = LaserBullet(self.x + self.width // 2, self.y + self.height // 2, angle, self.bullet_config)
            return self.laser_bullet
        return None

    def take_damage(self, damage):
        Player.add_score(self, -200)  # Deduct score when taking damage
        if self.invulnerable_timer <= 0:  # Only take damage if not invulnerable
            self.health -= damage
            self.score -= 100
            self.invulnerable_timer = 1000  # 1000 milliseconds of invulnerability
            

    def update(self, fps):
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1000 / fps  # Decrease timer based on FPS

        if self.laser_bullet and self.laser_bullet.should_remove():
            self.laser_bullet = None

    def draw(self, screen):
        if self.sprite:
            # Centro do player
            center_x = self.x + self.width // 2
            center_y = self.y + self.height // 2
            mouse_x, mouse_y = pygame.mouse.get_pos()
            target_angle = -math.degrees(math.atan2(mouse_y - center_y, mouse_x - center_x)) - 90

            if self.laser_bullet and (self.laser_bullet.charging or self.laser_bullet.fired):
                self.rotation_speed = 0.3  # Mais pesado ao girar
            else:
                self.rotation_speed = 5

            # Normaliza os ângulos para evitar rotações longas
            diff = (target_angle - self.rotation_angle + 180) % 360 - 180
            # Calcula o ângulo em graus (ajuste -90 para alinhar o topo da sprite)
            angle = -math.degrees(math.atan2(mouse_y - center_y, mouse_x - center_x)) - 90

            if abs(diff) < self.rotation_speed:
                self.rotation_angle = target_angle
            else:
                self.rotation_angle += self.rotation_speed * (1 if diff > 0 else -1)

            # Rotaciona suavemente
            rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation_angle)
            rotated_rect = rotated_sprite.get_rect(center=(center_x, center_y))

            # Pisca se invulnerável
            if self.invulnerable_timer > 0:
                if int(pygame.time.get_ticks() / 100) % 2 == 0:
                    screen.blit(rotated_sprite, rotated_rect.topleft)
            else:
                screen.blit(rotated_sprite, rotated_rect.topleft)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

    def draw_player_idle_animation(surface, sprite, center_x, center_y, amplitude=30, speed=2):
        """
        Desenha o sprite girando de um lado para o outro no centro da tela.
        amplitude: ângulo máximo de rotação (graus)
        speed: velocidade do balanço
        """
        t = pygame.time.get_ticks() / 1000  # tempo em segundos
        angle = math.sin(t * speed) * amplitude  # ângulo oscilando entre -amplitude e +amplitude

        rotated_sprite = pygame.transform.rotate(sprite, angle)
        rotated_rect = rotated_sprite.get_rect(center=(center_x, center_y))
        surface.blit(rotated_sprite, rotated_rect.topleft)