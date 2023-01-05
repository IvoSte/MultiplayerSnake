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

    def apply(self, snake):
        pass

    def remove(self, snake):
        pass


class SpeedPowerUp(PowerUp):
    def __init__(self, pos):
        super().__init__(pos)
        self.color = pygame.Color(255, 255, 0)
        self.name = "speed"
        self.duration = 30
        self.speedboost = 2.0

    def apply(self, snake):
        snake.speed *= self.speedboost

    def remove(self, snake):
        snake.speed /= self.speedboost


class GhostPowerUp(PowerUp):
    def __init__(self, pos):
        super().__init__(pos)
        self.color = pygame.Color(255, 255, 255)
        self.name = "ghost"
        self.duration = 180

    def apply(self, snake):
        snake.is_ghost = True

    def remove(self, snake):
        snake.is_ghost = False


class ShieldPowerUp(PowerUp):
    def __init__(self, pos):
        super().__init__(pos)
        self.color = pygame.Color(0, 0, 255)
        self.name = "shield"
        self.duration = 600
        self.shield_length = 30

    def apply(self, snake):
        snake.shield_length += self.shield_length

    def remove(self, snake):
        snake.shield_length -= self.shield_length
