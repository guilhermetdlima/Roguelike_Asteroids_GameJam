import pygame

class itens:
    def __init__(self, name, price, effect_function, rarity):
        self.rarity = rarity
        self.name = name
        self.price = price
        self.effect_function = effect_function
        self.bought = False
        
    def apply(self, player):
        self.effect_function(player)

    