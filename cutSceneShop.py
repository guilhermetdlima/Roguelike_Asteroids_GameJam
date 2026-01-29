import pygame

def draw_text(screen, text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


class CutSceneShop:

    def __init__(self, player, bullets, laser_bullets, enemies, screen_width):
        self.name = 'teste1'
        self.step = 0
        self.timer = pygame.time.get_ticks()
        self.cut_scene_running = True

        self.player = player
        self.bullets = bullets
        self.laser_bullets = laser_bullets
        self.enemies = enemies
        self.screen_width = screen_width 

        self.text = {
            "one": "Fase completada!",
            "two": "Indo a loja galatica.",
        }
        self.text_counter = 0

    def update(self):
        self.bullets.clear()
        self.laser_bullets.clear()
        self.enemies.clear()
        pressed = pygame.key.get_pressed()
        space = pressed[pygame.K_SPACE]
        if self.step == 0:
            if int(self.text_counter) < len(self.text['one']):
               self.text_counter += 0.4
            else:
                if space:
                    self.step = 1

        elif self.step == 1:
            if int(self.text_counter) < len(self.text['two']):
                self.text_counter += 0.4
            else:
                if space:
                    self.step = 2
                elif self.step == 2:
                    target_x = self.screen_width // 2 - self.player.width // 2
                    if self.player.x < target_x:
                        self.player.set_position(self.player.x + 10, self.player.y)
                    else:
                        self.player.set_position(target_x, self.player.y)
                self.step = 3

        elif self.step == 3:
            if space:
                self.step = 4
                
        elif self.step == 4:
            self.player.set_position(self.player.x + 10, self.player.y)
            if self.player.x > self.screen_width:
                self.cut_scene_running = False

                    
        return self.cut_scene_running
                    
    def draw(self, screen):
        if self.step == 0:
            draw_text(
                screen,
                self.text['one'][0:int(self.text_counter)],
                50,
                (255, 255, 255),
                self.screen_width // 2,
                50
            )
        if self.step == 1:
            draw_text(
                screen,
                self.text['two'][0:int(self.text_counter)],
                50,
                (255, 255, 255),
                self.screen_width // 2,
                50
            )