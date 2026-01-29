import pygame
import math

from bulletConfig import BulletConfig

class Bullet:
    def __init__(self, x, y, angle, config: BulletConfig, isCrit=0, spritesheet=None, frame_width=6, frame_height=6, num_frames=2):
        self.x = x
        self.y = y
        self.angle = math.radians(angle)
        self.config = config

        self.speed = config.speed
        self.damage = config.damage
        self.size = config.size
        self.bounce = config.bounce
        self.pierce = config.pierce
        self.rubber = None

        self.isCrit = isCrit

        self.vel_x = math.cos(self.angle) * self.speed
        self.vel_y = math.sin(self.angle) * self.speed

        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.rect.center = (self.x, self.y)

        self.pierced_enemies = {}
        self.target_enemy = None
        self.has_target = False
        self.homing_radius = 200

        # Animation
        self.spritesheet = spritesheet
        #print("Bullet spritesheet:", spritesheet)
        self.anim_frame = 0
        self.anim_speed = 120  # ms per frame
        self.last_anim_update = pygame.time.get_ticks()
        self.frames = []

        if self.spritesheet is not None:
            sheet_width = self.spritesheet.get_width()
            sheet_height = self.spritesheet.get_height()
            num_frames = sheet_width // frame_width  # override to avoid out-of-bounds
            for i in range(num_frames):
                frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
                if frame_rect.right <= sheet_width and frame_rect.bottom <= sheet_height:
                    frame = self.spritesheet.subsurface(frame_rect)
                    if frame.get_width() != self.size or frame.get_height() != self.size:
                        frame = pygame.transform.smoothscale(frame, (self.size, self.size))
                    self.frames.append(frame)

        #print("Bullet spritesheet:", self.spritesheet)
        #print("Frames loaded:", len(self.frames))

    def update(self, enemies=[]):
        if self.config.homing and enemies:
            close_enemies = [e for e in enemies if math.hypot(e.x - self.x, e.y - self.y) <= self.homing_radius]
            if not self.has_target and close_enemies:
                self.target_enemy = min(close_enemies, key=lambda e: math.hypot(e.x - self.x, e.y - self.y))
                self.has_target = True
            if self.target_enemy not in enemies:
                self.target_enemy = None
            if self.target_enemy:
                dx = self.target_enemy.x - self.x
                dy = self.target_enemy.y - self.y
                desired_angle = math.atan2(dy, dx)
                turn_speed = 0.3
                angle_diff = (desired_angle - self.angle + math.pi) % (2 * math.pi) - math.pi
                self.angle += angle_diff * turn_speed
                self.angle %= 2 * math.pi

        self.vel_x = math.cos(self.angle) * self.speed
        self.vel_y = math.sin(self.angle) * self.speed
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.center = (self.x, self.y)

        # Animation update
        if self.spritesheet is not None and self.frames:
            now = pygame.time.get_ticks()
            if now - self.last_anim_update > self.anim_speed:
                self.anim_frame = (self.anim_frame + 1) % len(self.frames)
                self.last_anim_update = now

    def draw(self, screen):
        if self.spritesheet is not None and self.frames:
            frame = self.frames[self.anim_frame]
            sprite_rect = frame.get_rect(center=self.rect.center)
            screen.blit(frame, sprite_rect)
        else:
            # Draw original yellow square
            pygame.draw.rect(screen, (255, 255, 0), self.rect)

    def is_off_screen(self, screen_width, screen_height):
        if self.bounce > 0:
            if self.x <= 0 or self.x >= screen_width:
                self.angle = math.pi - self.angle
                self.bounce -= 1
                return False
            if self.y <= 0 or self.y >= screen_height:
                self.angle = -self.angle
                self.bounce -= 1
                return False
        return (self.x < 0 or self.x > screen_width or
                self.y < 0 or self.y > screen_height)