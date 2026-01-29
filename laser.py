import pygame
import math

from bulletConfig import BulletConfig

class LaserBullet:

    def __init__(self, x, y, angle, config, charge_time=60):
        self.x = x
        self.y = y
        self.angle = math.radians(angle)
        self.config = config
        self.charge_time = charge_time  # frames to charge
        self.charging = True
        self.charge_counter = 0
        self.fired = False

        #self.rect = pygame.Rect(0, 0, self.size, self.size)

        self.length = 1536  # Laser length
        self.width = 80    # Laser width
        self.damage = config.damage * 5  # Massive damage
        self.cooldown = config.cooldown * 3

    def update_laser(self):
        if self.charging:
            self.charge_counter += 1
            if self.charge_counter >= self.charge_time:
                self.charging = False
                self.fired = True
                self.spawn_time = pygame.time.get_ticks()

    def update_position(self, x, y, angle, smoothing=0.15):
            self.x = x
            self.y = y
            target_angle = math.radians(angle)
            # Smoothly interpolate angle
            diff = (target_angle - self.angle + math.pi) % (2 * math.pi) - math.pi
            self.angle += diff * smoothing

    def should_remove(self):
        if self.fired:
            current_time = pygame.time.get_ticks()
            # Remove after 300 ms (adjust as needed)
            return current_time - self.spawn_time > 3000
        return False

    def draw(self, screen):
        if self.charging:
            # Draw a charging indicator (e.g., a growing circle)
            pygame.draw.circle(screen, (0, 255, 255), (int(self.x), int(self.y)), 20 + self.charge_counter // 2, 2)
        elif self.fired:
            # Draw the laser beam
            end_x = self.x + math.cos(self.angle) * self.length
            end_y = self.y + math.sin(self.angle) * self.length
            pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), (end_x, end_y), self.width)

