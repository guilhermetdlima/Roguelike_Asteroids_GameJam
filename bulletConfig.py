import random

class BulletConfig:
    def  __init__(self, type = "bala", homing = False, critC=0, speed=10, damage=1, size=15, cooldown=0.5, spread=0, effects=None, multB = 1, numB = 1, bomb = False):
        self.homing = homing
        self.bomb = bomb
        self.speed = speed
        self.damage = damage
        self.size = size
        self.cooldown = cooldown
        self.spread = spread
        self.bounce = 0
        self.pierce = 0
        self.effects = effects if effects is not None else set()
        self.multB = multB
        self.numB = numB
        self.type = type
        self.critC = critC