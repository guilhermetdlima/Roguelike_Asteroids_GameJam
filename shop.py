import random
import pygame
import time
from itens import itens
from cutSceneManager import CutSceneManager
from cutSceneExitShop import CutSceneExitShop


class shopMenu:

    def __init__(self, screen, font, all_itens):
        self.screen = screen
        self.font = font
        self.all_itens = all_itens
        self.rerrols = 1
        self.item_rects = []
        self.reroll_rect = None
        self.buy_button_rect = None
        self.selected_index = 0
        self.last_buy_time = 0  # cooldown para compra
        self.buy_cooldown = 300  # em milissegundos (0.3 segundos)
        self.last_reroll_time = 0
        self.reroll_cooldown = 300
        self.reroll_options()

    def reroll_options(self):
        self.itens = random.sample(self.all_itens, 3)
        for item in self.itens:
            item.bought = False
        self.selected_index = 0

    def show_shop(self, player, SCREEN, font):
        self.item_rects = []

        title = self.font.render("Loja", True, (255, 255, 255))
        self.screen.blit(title, (SCREEN.get_width() // 2 - title.get_width() // 2, 50))
    
        

        # Rect settings
        rect_w, rect_h = 320, 180
        spacing = 30
        total_w = 3 * rect_w + 2 * spacing
        start_x = (SCREEN.get_width() // 2 - total_w // 2) - 230
        y = SCREEN.get_height() // 2 - rect_h // 2

        for i, item in enumerate(self.itens):
            x = start_x + i * (rect_w + spacing)
            rect = pygame.Rect(x, y, rect_w, rect_h)
            self.item_rects.append((rect, item))

            # Highlight selected
            border_color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            pygame.draw.rect(SCREEN, (40, 40, 40), rect)
            pygame.draw.rect(SCREEN, border_color, rect, 4)

            # Item text
            color = (192, 192, 192) if item.bought else (255, 255, 255)
            name_text = self.font.render(f"{item.name}", True, color)
            price_text = self.font.render(f"Preço: ${item.price}", True, color)
            rarity_text = self.font.render(f"Raridade: {item.rarity}", True, color)
            SCREEN.blit(name_text, (x + 10, y + 30))
            SCREEN.blit(price_text, (x + 10, y + 80))
            SCREEN.blit(rarity_text, (x + 10, y + 130))

        # Buy button (bottom left)
        self.buy_button_rect = pygame.Rect(40, SCREEN.get_height() - 100, 200, 60)
        pygame.draw.rect(SCREEN, (0, 180, 0), self.buy_button_rect)
        pygame.draw.rect(SCREEN, (255, 255, 255), self.buy_button_rect, 3)
        buy_text = self.font.render("Comprar", True, (255, 255, 255))
        SCREEN.blit(buy_text, (self.buy_button_rect.x + 40, self.buy_button_rect.y + 15))

        # Reroll button (bottom right)
        self.reroll_rect = pygame.Rect(SCREEN.get_width() - 240, SCREEN.get_height() - 100, 200, 60)
        pygame.draw.rect(SCREEN, (0, 200, 200), self.reroll_rect)
        pygame.draw.rect(SCREEN, (255, 255, 255), self.reroll_rect, 3)
        reroll_text = self.font.render(f"Reroll ({self.rerrols})", True, (255, 255, 255))
        SCREEN.blit(reroll_text, (self.reroll_rect.x + 30, self.reroll_rect.y + 15))

        

    def handle_mouse_click(self, pos, player):
        now = pygame.time.get_ticks()
        clicked_any = False

        # Seleciona item
        for i, (rect, item) in enumerate(self.item_rects):
            if rect.collidepoint(pos):
                self.selected_index = i
                print(f"Selecionado: {item.name}")
                clicked_any = True
                break

        # Comprar item selecionado (com cooldown)
        if self.buy_button_rect and self.buy_button_rect.collidepoint(pos):
            if now - self.last_buy_time >= self.buy_cooldown:
                item = self.itens[self.selected_index]
                if not item.bought and player.money >= item.price:
                    player.money -= item.price
                    item.apply(player)
                    item.bought = True
                    print(f"{item.name} comprado!")
                    # Se for lendário, remove da lista de itens disponíveis
                    if item.rarity == "Léndario":
                        self.all_itens = [i for i in self.all_itens if i.name != item.name]
                        self.itens = [i for i in self.itens if i.name != item.name]
                elif item.bought:
                    print("Item já comprado!")
                else:
                    print("Dinheiro insuficiente!")
                self.last_buy_time = now
            else:
                print("Aguarde o cooldown para comprar novamente!")
            clicked_any = True

        if self.reroll_rect and self.reroll_rect.collidepoint(pos):
            if now - self.last_reroll_time >= self.reroll_cooldown:
                if player.money >= self.rerrols:
                    player.money -= self.rerrols
                    self.rerrols += 1
                    self.reroll_options()
                    print("Itens rerolados")
                else:
                    print("Dinheiro insuficiente para Reroll!")
                self.last_reroll_time = now
            else:
                print("Aguarde o cooldown do reroll!")
            clicked_any = True


        if not clicked_any:
            print("Clique fora dos itens/botões.")

    def reset_shop(self):
        self.rerrols = 1
