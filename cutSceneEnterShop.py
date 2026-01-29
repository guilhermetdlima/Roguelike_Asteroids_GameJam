import pygame
def draw_text(screen, text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

class CutSceneEnterShop:
    def __init__(self, player, screen_width):
        self.name = "enter_shop"
        self.player = player
        self.screen_width = screen_width
        self.cut_scene_running = True
        self.text = {
            "one": "Aperta espaço para abrir a loja!",
        }
        self.text_counter = 0
        self.center = False

    def update(self):
        # Move player to center
        pressed = pygame.key.get_pressed()
        target_x = self.screen_width // 2 - self.player.width // 2
        if abs(self.player.x - target_x) <= 3:
            if int(self.text_counter) < len(self.text['one']):
               self.text_counter += 0.4
            self.player.set_position(target_x, self.player.y)
            self.center = True
            if pressed[pygame.K_SPACE]:
                self.cut_scene_running = False
        else:
            direction = 10 if self.player.x < target_x else -3
            self.player.set_position(self.player.x + direction, self.player.y)
        return self.cut_scene_running

    def draw(self, screen):
        if self.center:
            draw_text(
                screen,
                self.text['one'][0:int(self.text_counter)],
                50,
                (255, 255, 255),
                self.screen_width // 2,
                50
            )