from entities.item import Item
import pygame
from game.config import config
from math import pi

x, y = (
    config["GAME"]["BLOCK_SIZE"] * config["GAME"]["RESOLUTION_SCALE"],
    config["GAME"]["BLOCK_SIZE"] * config["GAME"]["RESOLUTION_SCALE"],
)
bolt_shape = [
    (x / 2, 0),
    (x, 0),
    (x / 2, y / 3),
    (x, y / 3),
    (0, y),
    (x / 2, y / 2),
    (0, y / 2),
]


class PowerUp(Item):
    def __init__(self, pos):
        super().__init__()
        self.size = (
            config["GAME"]["BLOCK_SIZE"] * config["GAME"]["RESOLUTION_SCALE"],
            config["GAME"]["BLOCK_SIZE"] * config["GAME"]["RESOLUTION_SCALE"],
        )
        self.color = pygame.Color(0, 0, 0)
        self.pos = pos
        self.initial_duration = 0
        self.duration = self.initial_duration

    def update(self):
        self.duration -= 1

    def is_expired(self):
        return self.duration <= 0

    def apply(self, snake):
        pass

    def remove(self, snake):
        pass

    def draw(self):
        surface = pygame.Surface(self.size)
        pygame.draw.rect(surface, self.color, [0, 0, *self.size])
        return surface

    def draw_counter_square(self):
        surface = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.rect(surface, pygame.Color(0, 0, 0, 100), [0, 0, *self.size])
        pygame.draw.rect(
            surface,
            self.color,
            [0, 0, self.fraction_left * self.size[0], self.size[1]],
        )
        return surface

    def draw_counter_circle(self):
        surface = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.arc(
            surface,
            self.color,
            [0, 0, *self.size],
            start_angle=0.0,
            stop_angle=self.fraction_left * (2 * pi),
            width=5,
        )
        return surface

    @property
    def fraction_left(self):
        return self.duration / self.initial_duration


class SpeedPowerUp(PowerUp):
    def __init__(self, pos):
        super().__init__(pos)
        self.color = pygame.Color(255, 255, 0)
        self.name = "speed"
        self.initial_duration = 30
        self.duration = self.initial_duration
        self.speedboost = 2.0

    def apply(self, snake):
        snake.speed *= self.speedboost

    def remove(self, snake):
        snake.speed /= self.speedboost

    def draw(self):
        surface = pygame.Surface(self.size, pygame.SRCALPHA)

        # Version 1 -- Bolt with background
        # pygame.draw.rect(surface, pygame.Color(173, 31, 21, 250), [0, 0, *self.size], 8)
        pygame.draw.polygon(surface, self.color, bolt_shape)

        # Version 2 -- Yellow with border
        # pygame.draw.rect(surface, self.color, [0, 0, *self.size])
        # pygame.draw.rect(
        #     surface, pygame.Color(0, 0, 0), [0, 0, *self.size], 4, border_radius=0
        # )
        return surface


class GhostPowerUp(PowerUp):
    def __init__(self, pos):
        super().__init__(pos)
        self.color = pygame.Color(255, 255, 255)
        self.name = "ghost"
        self.initial_duration = 180
        self.duration = self.initial_duration

    def apply(self, snake):
        snake.is_ghost = True

    def remove(self, snake):
        snake.is_ghost = False

    def draw(self):
        surface = pygame.Surface(self.size, pygame.SRCALPHA)
        x, y = self.size
        pygame.draw.rect(
            surface, pygame.Color(255, 255, 255, 255), [0, 0, 1 * x / 4, y]
        )
        pygame.draw.rect(
            surface, pygame.Color(255, 255, 255, 200), [1 * x / 4, 0, 2 * x / 4, y]
        )
        pygame.draw.rect(
            surface, pygame.Color(255, 255, 255, 150), [2 * x / 4, 0, 3 * x / 4, y]
        )
        pygame.draw.rect(
            surface, pygame.Color(255, 255, 255, 100), [3 * x / 4, 0, 4 * x / 4, y]
        )
        # pygame.draw.ellipse(surface, self.color, [0, 0, self.size[0], self.size[1]])
        return surface


class ShieldPowerUp(PowerUp):
    def __init__(self, pos):
        super().__init__(pos)
        self.color = pygame.Color(14, 100, 180)
        self.name = "shield"
        self.initial_duration = 600
        self.duration = self.initial_duration
        self.shield_length = 5

    def apply(self, snake):
        snake.shield_length += self.shield_length

    def remove(self, snake):
        snake.shield_length -= self.shield_length

    def draw(self):
        surface = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.rect(surface, self.color, [0, 0, self.size[0], self.size[1] / 2])
        pygame.draw.ellipse(surface, self.color, [0, 0, self.size[0], self.size[1]])
        return surface
