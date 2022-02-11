from colors import Color, colormaps
from input_controls import Controls, default_player_controls
import pygame
import random

class Player:
    def __init__(self, x_pos, y_pos, speed=15, width=10, length=1, color=random.randint(0, 255), colormap = random.choice(colormaps), colorscale=random.randint(0, 3), score=0, name="Player", controls=default_player_controls):
        self.name = name
        self.controls = controls
        
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed = speed
        self.body = [(x_pos, y_pos)]
        self.width = width
        self.length = length
        self.color = color
        self.colormap = colormap
        self.colorscale = colorscale

        self.score = score
        self.alive = True
        self.command = None
        self.move_dir_buffer = None
        self.move_dist_buffer = 0


    def set_command(self, command):
        if self.check_legal_move(command):
            self.command = command

    def update_body(self):
        # Update total body positions
        self.body.append((self.x_pos, self.y_pos))
        if len(self.body) > self.length:
            self.body.pop(0)

    def is_dead(self, display_size, snakes = None):
        if snakes == None:
            snakes = [self]
        # hit edges/boundaries
        if self.x_pos >= display_size[0] or self.x_pos < 0 or self.y_pos >= display_size[1] or self.y_pos < 0:
            print(f"{self.name} hit the edge and died")
            self.alive = False

        # Snake dies because it hits itself
        for other in snakes:
            if self.collision(other):
                print(f"{self.name} booped a snake with its snoot, perishing in the process.")
                self.alive = False

    def collision(self, other) -> bool:
        # Collision if my head is in your body, we collided. You can be me
        # TODO head collisions are acceptable
        return self.body[len(self.body) - 1] in other.body[0:len(other.body) - 2]

    def move(self):
        # The move command is issued each tick. This function translates that check to the move speed
        # Updating the direction at required points
        if self.x_pos % self.width == 0 and self.y_pos % self.width == 0:
            self.move_dir_buffer = self.command
        self.move_step(self.width / self.speed)

    def move_step(self, step_size):
        # Determine move direction
        if self.move_dir_buffer == None:
            x_pos_change = 0
            y_pos_change = 0
        elif self.move_dir_buffer == Controls.LEFT:
            x_pos_change = -step_size
            y_pos_change = 0
        elif self.move_dir_buffer == Controls.RIGHT:
            x_pos_change = step_size
            y_pos_change = 0
        elif self.move_dir_buffer == Controls.UP:
            y_pos_change = -step_size
            x_pos_change = 0
        elif self.move_dir_buffer == Controls.DOWN:
            y_pos_change = step_size
            x_pos_change = 0
        else :
            x_pos_change = 0
            y_pos_change = 0

        # current position of player head
        self.x_pos += x_pos_change
        self.y_pos += y_pos_change

    def eat_food(self, food) -> bool:
        # TODO possibly should not be checked here but one place higher. This also works
        if self.body[len(self.body)-1] == food.pos:
            self.length += 1
            self.score += 1
            food.notify() # Spawn another random food
            return True
        return False

    def check_legal_move(self, command):
        if command == Controls.UP and self.move_dir_buffer == Controls.DOWN:
            return False
        if command == Controls.DOWN and self.move_dir_buffer == Controls.UP:
            return False
        if command == Controls.LEFT and self.move_dir_buffer == Controls.RIGHT:
            return False
        if command == Controls.RIGHT and self.move_dir_buffer == Controls.LEFT:
            return False
        return True
        
