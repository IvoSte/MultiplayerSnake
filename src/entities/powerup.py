from entities.item import Item
import pygame


class PowerUp(Item):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.duration = 0

    def update(self):
        self.duration -= 1

    def is_expired(self):
        return self.duration <= 0


class SpeedPowerUp(PowerUp):
    def __init__(self, pos):
        super().__init__(pos)
        self.color = pygame.Color(255, 255, 0)
        self.name = "speed"
        self.duration = 60
        self.speedboost = -0.0
