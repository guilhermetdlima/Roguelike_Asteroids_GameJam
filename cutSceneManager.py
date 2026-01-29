import pygame
class CutSceneManager:

    def __init__(self, screen):
        self.cut_scene_complete = []
        self.cut_scene = None
        self.cut_scene_running = False
    
        # Variaveis de desenho
        self.screen = screen
        self.window_size = 0
    
    def start_cut_scene(self, cut_scene):
        self.cut_scene = cut_scene
        self.cut_scene_running = True
        
    def end_cut_scene(self):
        self.cut_scene = None
        self.cut_scene_running = False

    def update(self):
        if self.cut_scene_running:
            if self.window_size < self.screen.get_height() * 0.3:
                self.window_size += 3
            still_running = self.cut_scene.update()
            if not still_running:
                self.end_cut_scene()

    def draw(self):
        if self.cut_scene_running:
            pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.screen.get_width(), int(self.window_size)))
            self.cut_scene.draw(self.screen)