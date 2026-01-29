from baseAsteroid import BaseAsteroid
from fastAsteroid import FastAsteroid
from tankAsteroid import TankAsteroid
from multAsteroid import MultAsteroid
from stealthAsteroid import StealthAsteroid
from superTankAsteroid import SuperTankAsteroid
from bossAsteroid1 import BossAsteroid1
from bossShooter import BossShooter
from bossShooterL import BossShooterL
from lightningAsteroid import LightningAsteroid
from player import Player
from math import trunc
from bullet import Bullet
from bulletConfig import BulletConfig
import pygame
import math




class LevelManager:
    def __init__(self, screen_width, screen_height):
        self.current_level = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.levels = self.define_levels()
        self.mult = 0.01

    def define_levels(self):
        # Define enemy configurations for each level
        return {
            #1: [BaseAsteroid, BaseAsteroid, BaseAsteroid],
            1: [FastAsteroid, BossShooter],
            2: [BaseAsteroid, FastAsteroid, FastAsteroid],
            3: [FastAsteroid, TankAsteroid, FastAsteroid, FastAsteroid],

            4: [TankAsteroid, MultAsteroid],
            5: [MultAsteroid, MultAsteroid, FastAsteroid],
            6: [MultAsteroid, MultAsteroid, MultAsteroid, MultAsteroid, MultAsteroid,],
            7: [MultAsteroid, FastAsteroid, FastAsteroid, FastAsteroid, FastAsteroid, MultAsteroid],

            8: [TankAsteroid, TankAsteroid, BaseAsteroid, BaseAsteroid, FastAsteroid, FastAsteroid],
            9: [TankAsteroid, TankAsteroid, FastAsteroid, FastAsteroid, FastAsteroid, FastAsteroid, BaseAsteroid],
            10: [TankAsteroid,TankAsteroid, TankAsteroid, TankAsteroid, TankAsteroid, TankAsteroid, TankAsteroid, TankAsteroid, TankAsteroid, TankAsteroid,  ],
            11: [TankAsteroid, TankAsteroid, BossAsteroid1],

            12: [MultAsteroid, MultAsteroid, MultAsteroid, MultAsteroid, MultAsteroid, FastAsteroid, FastAsteroid, FastAsteroid, FastAsteroid, FastAsteroid],
            13: [FastAsteroid, FastAsteroid, FastAsteroid, FastAsteroid, FastAsteroid, FastAsteroid, FastAsteroid, FastAsteroid, FastAsteroid, FastAsteroid, FastAsteroid, FastAsteroid, ],
            14: [BossAsteroid1, MultAsteroid, MultAsteroid, FastAsteroid],
            15: [BossAsteroid1, BossAsteroid1],
            
            16: [BossAsteroid1, LightningAsteroid, LightningAsteroid, LightningAsteroid, LightningAsteroid, TankAsteroid, TankAsteroid],
            17: [LightningAsteroid, LightningAsteroid, SuperTankAsteroid, SuperTankAsteroid, FastAsteroid, MultAsteroid],
            18: [StealthAsteroid, StealthAsteroid, StealthAsteroid, StealthAsteroid, StealthAsteroid, SuperTankAsteroid, SuperTankAsteroid],
            19: [BossAsteroid1, BossAsteroid1, BossAsteroid1, SuperTankAsteroid, SuperTankAsteroid, SuperTankAsteroid, SuperTankAsteroid,],

            20: [BossShooter, StealthAsteroid, StealthAsteroid, StealthAsteroid],
            21: [LightningAsteroid, LightningAsteroid, LightningAsteroid, LightningAsteroid, LightningAsteroid, LightningAsteroid, LightningAsteroid, LightningAsteroid],
            22: [BaseAsteroid, BaseAsteroid, FastAsteroid, FastAsteroid, TankAsteroid, TankAsteroid, MultAsteroid, MultAsteroid, StealthAsteroid, StealthAsteroid, LightningAsteroid, LightningAsteroid, SuperTankAsteroid, SuperTankAsteroid],
            23: [BossAsteroid1, BossAsteroid1, BossAsteroid1, BossAsteroid1, BossAsteroid1, BossAsteroid1, BossAsteroid1, BossAsteroid1],

            24: [BossShooter, BossShooterL],
            25: []
            
        }

    def get_enemies_for_level(self):
        # Get the enemy classes for the current level
        if self.current_level in self.levels:
            return self.levels[self.current_level]
        return []

    def spawn_enemies(self, player, bullet_config, selected_difficulty, bossSprite=None, bossBulletSprite=None):
        diff = 0
        if selected_difficulty == "Medium":
            diff = 0.5
        elif selected_difficulty == "Hard":
            diff = 1
        enemies = []
        for enemy_class in self.get_enemies_for_level():
            print("BALA SPRITE LEVELMANAGER:", bossBulletSprite)
            if enemy_class is BossShooter or enemy_class is BossShooterL:
                enemies.append(enemy_class(
                    self.screen_width, self.screen_height, player, 1 + self.mult + diff, bullet_config, bossSprite, bossBulletSprite))
            else:
                enemies.append(enemy_class(self.screen_width, self.screen_height, 1 + self.mult + diff))
        return enemies

    def next_level(self, player):
        self.mult += 0.03
        player.money += trunc(4) 
        if (1/10)*player.money > 5:
            player.money += trunc(5)
        else:
            player.money += trunc(1/10)*player.money
        self.current_level += 1

    