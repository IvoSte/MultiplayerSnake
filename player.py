from colors import Color
from input_controls import Controls, inputHandler
import pygame

class Player:
    def __init__(self, x_pos, y_pos, speed=15, width = 10, length = 1, score = 0, name = "ivo Schmabe <- noobie guy"):
        self.name = name
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed = speed
        self.body = [(x_pos, y_pos)]
        self.score = score
        self.width = width
        self.length = length
        self.alive = True
        self.command = None

    def set_command(self, command):
        self.command = command

    def update_body(self):
        # Update total body positions
        self.body.append((self.x_pos, self.y_pos))
        if len(self.body) > self.length:
            self.body.pop(0)

    def is_dead(self, display_size, snakes = None) -> bool:
        if snakes == None:
            snakes = [self]
        # hit edges/boundaries
        if self.x_pos >= display_size[0] or self.x_pos < 0 or self.y_pos >= display_size[1] or self.y_pos < 0:
            return True

        # Snake dies because it hits itself
        for other in snakes:
            if self.collision(other):
                return True

    def collision(self, other) -> bool:
        # Collision if my head is in your body, we collided. You can be me
        # TODO head collisions are acceptable
        return self.body[len(self.body) - 1] in other.body[0:len(other.body) - 2]

    def move(self):
        # Determine move direction
        if self.command == None:
            x_pos_change = 0
            y_pos_change = 0
        elif self.command == Controls.LEFT:
            x_pos_change = -self.width
            y_pos_change = 0
        elif self.command == Controls.RIGHT:
            x_pos_change = self.width
            y_pos_change = 0
        elif self.command == Controls.UP:
            y_pos_change = -self.width
            x_pos_change = 0
        elif self.command == Controls.DOWN:
            y_pos_change = self.width
            x_pos_change = 0

        # current position of player head
        self.x_pos += x_pos_change
        self.y_pos += y_pos_change

    def eat_food(self, food):
        # TODO possibly should not be checked here but one place higher. This also works
        if self.body[len(self.body)-1] == food.pos:
            self.length += 1
            self.score += 1
            food.notify() # Spawn another random food
