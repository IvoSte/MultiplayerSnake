from viewer.colors import Color, color_from_map, colormaps
from controls.input_controls import Controls, default_player_controls
import pygame
import random
from game.env_variables import (
    BODY_DECAY_RATE,
    DEATH_PUNISHMENT,
    FREEZE_FRAMES_ON_BITTEN,
    FREEZE_FRAMES_ON_EAT,
    SNAKE_SIZE,
    INITIAL_SNAKE_LENGTH,
    SNAKE_SPEED,
    MAX_COLOR_SCALE,
    START_COUNTDOWN,
    TAIL_BITING,
    TAIL_STEALING,
    TICKS_PER_SECOND,
    VERZET,
)
from game.config import config

class Snake:
    def __init__(
        self,
        x_pos,
        y_pos,
        speed=SNAKE_SPEED,
        width=SNAKE_SIZE,
        length=INITIAL_SNAKE_LENGTH,
        color=random.randint(0, 255),
        colormap=random.choice(list(colormaps.values())),
        colorscale=random.randint(1, MAX_COLOR_SCALE),
        score=0,
        lives=0,
        name="Snake",
        controls=default_player_controls,
    ):
        self.name = name
        self.controls = controls

        self.spawn_pos_x = x_pos
        self.spawn_pos_y = y_pos

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed = speed
        self.body = [(x_pos, y_pos)]
        self.decaying_body = []
        self.width = width
        self.length = length
        self.color = color
        self.colormap = colormap
        self.colorscale = colorscale
        self.head_color = color_from_map(colormap, color)
        self.decay_body_color = []

        self.score = score
        self.alive = True
        self.lives_left = lives
        self.command = None
        self.move_dir_buffer = None
        self.move_dist_buffer = 0
        self.move_freeze_timer = START_COUNTDOWN * TICKS_PER_SECOND
        self.body_buffer = 0

        self.ghost = False
        self.tails_lost = 0
        self.tails_eaten = 0

    def set_command(self, command):
        if self.check_legal_move(command):
            self.command = command

    def update_body(self):
        # Update total body positions
        if self.alive:
            self.body.append((self.x_pos, self.y_pos))
        while len(self.body) > self.body_length():
            self.body.pop(0)
        if len(self.decaying_body) > 0:
            self.update_decaying_body()

    def body_length(self):
        return self.length * self.speed

    def update_decaying_body(self):
        ## TODO Here stuff can go wrong if the decay rate is set different. I dislike working with these colours.
        if self.decay_body_color[0] == pygame.Color(0, 0, 0):
            self.decaying_body = []
            self.decay_body_color = []
        else:
            for idx in range(len(self.decaying_body)):
                c = self.decay_body_color[idx]
                self.decay_body_color[idx] = pygame.Color(
                    c.r - BODY_DECAY_RATE, c.g - BODY_DECAY_RATE, c.b - BODY_DECAY_RATE
                )

    def is_dead(self, grid_size, snakes=None):
        if snakes == None:
            snakes = [self]
        # hit edges/boundaries
        if (
            self.x_pos >= grid_size[0]
            or self.x_pos < 0
            or self.y_pos >= grid_size[1]
            or self.y_pos < 0
        ):
            # print(f"{self.name} hit the edge and died")
            self.init_decaying_body(self.body[0 : len(self.body)])
            self.alive = False

        # Snake dies because it hits itself
        for other in snakes:
            if config['mode']['tail_biting']:
                self.bite_collision(other)
            else:
                if self.collision(other):
                    # print(f"{self.name} booped a snake with its snoot, perishing in the process.")
                    self.init_decaying_body(self.body[0 : len(self.body)])
                    self.alive = False

    def collision(self, other) -> bool:
        # Collision if my head is in your body, we collided. You can be me
        # TODO head collisions are acceptable

        # If my head and neck are at the same position, don't check collisions
        # because it means I just spawned
        # TODO possibly index out of bounds issue here where it checks the neck if there is none.
        if self.body[len(self.body) - 1] == self.body[len(self.body) - 2]:
            return False

        # Collision with myself
        if other.name == self.name:
            return self.body[len(self.body) - 1] in other.body[0 : len(other.body) - 1]
        else:
            return self.body[len(self.body) - 1] in other.body

    def bite_collision(self, other):
        # Hatchling snek is friendly
        if self.body[len(self.body) - 1] == self.body[len(self.body) - 2]:
            return
        if self.body[len(self.body) - 1] in other.body[0 : len(other.body) - 1]:
            self.move_freeze_timer = FREEZE_FRAMES_ON_EAT
            # I bite you where my head is at
            tails_bitten = other.get_bitten(self.body[len(self.body) - 1])

            if other.name != self.name:
                self.tails_eaten += tails_bitten
                if TAIL_STEALING:
                    self.length += tails_bitten

    def get_bitten(self, pos):
        bite_position = self.body.index(pos)

        # Can't bite off my head
        if bite_position >= len(self.body) - (1 * self.speed):
            return 0

        tails_lost = (
            1 + (self.body_length() - ((len(self.body) - bite_position))) // self.speed
        )
        if VERZET:
            self.move_freeze_timer = FREEZE_FRAMES_ON_BITTEN
        self.init_decaying_body(self.body[0:bite_position])
        self.body = self.body[bite_position : len(self.body)]
        self.length = self.length - tails_lost
        self.tails_lost += tails_lost
        return tails_lost

    def init_decaying_body(self, decaying_body):
        self.decaying_body = decaying_body
        self.decay_body_color = [pygame.Color(255, 255, 255) for tail in decaying_body]

    def move(self):
        # The move command is issued each tick. This function translates that check to the move speed
        # Updating the direction at required points
        # if self.x_pos % self.width == 0 and self.y_pos % self.width == 0:
        step_size = 1.0 / self.speed
        # When x or y crosses to the next grid position, we can change direction.
        # NOTE: This gives problems at higher speeds, when floating point errors.
        if self.x_pos % 1.0 == 0.0 and self.y_pos % 1.0 == 0.0:
            self.move_dir_buffer = self.command
        if self.move_freeze_timer > 0:
            self.move_freeze_timer -= 1
        else:
            self.move_step(step_size)

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
        else:
            x_pos_change = 0
            y_pos_change = 0

        # current position of player head
        self.x_pos += x_pos_change
        self.y_pos += y_pos_change
        # print(f"Snake moved to {self.x_pos} {self.y_pos}")

    def eat_food(self, food) -> bool:
        # TODO possibly should not be checked here but one place higher. This also works
        if self.body[len(self.body) - 1] == food.pos:
            self.length += 1
            self.score += 1
            food.notify()  # Spawn another random food
            return True
        return False

    def check_legal_move(self, command):
        # Can't reverse
        if command == Controls.UP and self.move_dir_buffer == Controls.DOWN:
            return False
        if command == Controls.DOWN and self.move_dir_buffer == Controls.UP:
            return False
        if command == Controls.LEFT and self.move_dir_buffer == Controls.RIGHT:
            return False
        if command == Controls.RIGHT and self.move_dir_buffer == Controls.LEFT:
            return False
        return True

    def respawn(self, x_pos=None, y_pos=None, punishment=DEATH_PUNISHMENT):
        # Default spawn or given arguments
        x_pos = self.spawn_pos_x if x_pos == None else x_pos
        y_pos = self.spawn_pos_y if y_pos == None else y_pos

        # print(f"{self.name} respawning. {self.lives_left} lives left.")

        # Set alive
        self.alive = True

        # Cut off some of the tail
        self.length = self.length - punishment if self.length - punishment > 1 else 1

        self.command = None
        self.move_dir_buffer = None
        self.spawn(x_pos, y_pos)

    def spawn(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

        # Remove body at spawn. It will grow to length when starting to move.
        # Having only a head avoids collision with body at respawn
        self.body = [(x_pos, y_pos)]

    def report(self):
        print(f"Snake report: {self.name}")
        print(
            f"    {self.score = }\n   {self.length = }\n  {self.tails_lost = }\n  {self.tails_eaten = }"
        )
