import pygame

class CutSceneExitShop:
    def __init__(self, player, screen_width):
        self.name = "exit_shop"
        self.player = player
        self.screen_width = screen_width
        self.cut_scene_running = True

    def update(self):
        # Move player to the right
        self.player.set_position(self.player.x + 10, self.player.y)
        if self.player.x > self.screen_width:
            self.cut_scene_running = False
        return self.cut_scene_running

    def draw(self, screen):
        # No extra drawing needed, just the player
        pass
