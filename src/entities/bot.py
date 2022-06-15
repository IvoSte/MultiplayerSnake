from dataclasses import dataclass
import random
from typing import Optional

import pygame

from entities.player import Player
from entities.snake import Snake
from controls.input_controls import Controls, default_player_controls
from enum import Enum


@dataclass
class ObjectiveDistance:
    x: int
    y: int


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Bot(Player):
    def __init__(
        self,
        model,
        name="Bot",
        snake: Snake = None,
        controls=default_player_controls,
        snake_colormap=None,
    ):
        Player.__init__(self, name, snake, controls, snake_colormap)
        self.model = model
        # This can be done better (line below comment). For now it needs the keypress for a control it is 'supposed' to press as a player
        # it would be better to update the controller input handler to also handle all already converted inputs. TODO
        self.control_keys = {value: key for key, value in self.controls.items()}
        self.danger_distance: ObjectiveDistance
        self.goal_distance: ObjectiveDistance
        self.next_move: Controls

    def observe(self):
        self.find_danger()
        self.find_goal()

    def find_danger(self):
        pass

    def get_distance_to(self, direction, goal):
        pass

    def find_goal(self):
        # set minimum distance to any food object in x and y direction
        # clear previous distances and set them to the max
        self.objective_distance = ObjectiveDistance(
            x=self.model.grid_size[0], y=self.model.grid_size[1]
        )

        # For each food object, calculate the distance and overwrite the smallest distance
        # if it is closer than any previously encountered
        # TODO this is dumb, just find the closest food piece and move towards that, don't overwrite closest x or y, only both
        for food in self.model.food:
            dist_x, dist_y = self.find_distance(
                self.snake.x_pos, self.snake.y_pos, food.pos[0], food.pos[1]
            )
            if abs(dist_x) < abs(self.objective_distance.x):
                self.objective_distance.x = dist_x
            if abs(dist_y) < abs(self.objective_distance.y):
                self.objective_distance.y = dist_y

    def find_distance(self, x1, y1, x2, y2):
        dist_x = x2 - x1
        dist_y = y2 - y1
        return (dist_x, dist_y)

    def decide_policy(self):
        print(self.objective_distance)
        if self.objective_distance.x != 0.0:
            # Move horizontally
            if self.objective_distance.x > 0.0:
                self.next_move = Controls.RIGHT
            else:
                self.next_move = Controls.LEFT
        elif self.objective_distance.y != 0.0:
            # Move vertically
            if self.objective_distance.y > 0.0:
                self.next_move = Controls.DOWN
            else:
                self.next_move = Controls.UP
        #self.unstuck_impossible_move()

    def unstuck_impossible_move(self):
        if self.opposite_direction(self.next_move, self.snake.move_dir_buffer):
            print("UNSTUCKING MOVE")
            self.next_move = Controls(random.randint(0, 3))

    def opposite_direction(self, control_1, control_2):
        if control_1 == Controls.UP and control_2 == Controls.DOWN:
            return True
        if control_1 == Controls.DOWN and control_2 == Controls.UP:
            return True
        if control_1 == Controls.LEFT and control_2 == Controls.RIGHT:
            return True
        if control_1 == Controls.RIGHT and control_2 == Controls.LEFT:
            return True
        return False

    def execute_policy(self):
        key_event = pygame.event.Event(
            pygame.KEYDOWN, {"key": self.control_keys[self.next_move]}
        )
        pygame.event.post(key_event)

    def tick(self):
        self.observe()
        self.decide_policy()
        self.execute_policy()
