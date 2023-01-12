from viewer.colors import Color, color_from_map, colormaps
from controls.input_controls import Controls, default_player_controls
import pygame
import random
from game.config import config
from entities.food import Food
from entities.powerup import PowerUp, SpeedPowerUp
import math


class Snake:
    def __init__(
        self,
        x_pos,
        y_pos,
        speed=config["PLAYER"]["SNAKE_SPEED"],
        width=config["GAME"]["SNAKE_SIZE"] * config["game"]["RESOLUTION_SCALE"],
        length=config["PLAYER"]["INITIAL_SNAKE_LENGTH"],
        body_segment_density=config["GAME"]["SNAKE_BODY_SEGMENTS_PER_BLOCK"],
        color=random.randint(0, 255),
        colormap=random.choice(list(colormaps.values())),
        colorscale=random.randint(1, config["COSMETIC"]["MAX_COLOR_SCALE"]),
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
        self.body = [(x_pos, y_pos)] * length * body_segment_density
        self.decaying_body = []
        self.width = width
        self.length = length
        self.body_segment_density = (
            body_segment_density  # The number of segments per block
        )
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
        self.move_freeze_timer = (
            config["GAMEPLAY"]["START_COUNTDOWN"] * config["GAME"]["TICKS_PER_SECOND"]
        )
        self.body_buffer = 0
        self.body_decay_rate = config["COSMETIC"]["BODY_DECAY_RATE"]

        self.tails_lost = 0
        self.tails_eaten = 0

        self.powerups = []
        self.is_ghost = False
        self.shield_length = 0

    def set_command(self, command):
        if self.check_legal_move(command):
            self.command = command

    def update(self):
        self.update_powerups()
        self.update_decaying_body()

    def update_body(self):
        # Update total body positions
        if self.alive:
            self.body.append((self.x_pos, self.y_pos))
        while len(self.body) > self.body_length:
            self.body.pop(0)

    @property
    def body_length(self):
        return self.length * self.body_segment_density

    @property
    def head(self):
        return self.body[len(self.body) - 1]

    @property
    def neck(self):
        return self.body[len(self.body) - 2]

    @property
    def tail(self):
        # The tail is not just the tip, it is everything that is not the head
        return self.body[0 : self.body_length - self.body_segment_density]

    def update_decaying_body(self):
        if len(self.decaying_body) == 0:
            return
        ## TODO Here stuff can go wrong if the decay rate is set different. I dislike working with these colours.
        if self.decay_body_color[0] == pygame.Color(0, 0, 0):
            self.decaying_body = []
            self.decay_body_color = []
        else:
            for idx in range(len(self.decaying_body)):
                c = self.decay_body_color[idx]
                self.decay_body_color[idx] = pygame.Color(
                    c.r - self.body_decay_rate,
                    c.g - self.body_decay_rate,
                    c.b - self.body_decay_rate,
                )

    def is_dead(self, grid_size, snakes=None):
        if snakes == None:
            snakes = [self]
        # hit edges/boundaries
        if self.border_collision(grid_size):
            # print(f"{self.name} hit the edge and died")
            self.die()

        # Snake dies because it hits itself
        for other in snakes:
            if config["MODE"]["TAIL_BITING"]:
                self.bite_collision(other)
            else:
                if self.collision(other):
                    # print(f"{self.name} booped a snake with its snoot, perishing in the process.")
                    self.die()

    def die(self):
        self.init_decaying_body(self.body)
        self.alive = False

    def border_collision(self, grid_size):
        if (
            self.x_pos >= grid_size[0]
            or self.x_pos < 0
            or self.y_pos >= grid_size[1]
            or self.y_pos < 0
        ):
            return True
        return False

    def collision(self, other) -> bool:
        # Collision if my head is in your body, we collided. You can be me

        # If I am a ghost, I can't collide with anything
        if self.is_ghost or other.is_ghost:
            return False
        # TODO head collisions are acceptable

        # If my head and neck are at the same position, don't check collisions
        # because it means I just spawned
        if self.head == self.neck:
            return False

        # Collision with myself
        if other.name == self.name:
            return self.head in other.tail
        else:
            return self.head in other.body

    def bite_collision(self, other):
        if other.is_ghost:
            return
        # Hatchling snek is friendly (when head and neck are at the same place, we don't bite)
        if self.head == self.neck:
            return
        # I bite you where my head is at
        if self.head in other.tail:
            if other.position_is_shielded(pos=self.head):
                print(
                    f"{self.name} tried to bite {other.name} but got blocked by their shield"
                )
                self.die()
                return
            # Currently, don't freeze the frames, as now it will bring the snake in a loop, where it checks
            # keeps biting the same position, again adding the freeze frames. Biting one position more fixes the problem, but
            # makes for something uglier. Perhaps some other solution is needed (a small bite cooldown variable.)
            # The bug was introduced when changing the order or when the snake moves and when it checks for collisions.
            # self.move_freeze_timer = config["COSMETIC"]["FREEZE_FRAMES_ON_EAT"]
            tails_bitten = other.get_bitten(pos=self.head)

            if other.name != self.name:
                self.tails_eaten += tails_bitten
                if config["MODE"]["TAIL_STEALING"]:
                    self.length += tails_bitten

    def position_is_shielded(self, pos):
        bite_position = self.body.index(pos)
        return bite_position >= self.body_length - (
            self.shield_length * self.body_segment_density
        )

    def get_bitten(self, pos):
        bite_position = self.body.index(pos)

        # Can't bite off my protected body parts
        if self.position_is_shielded(pos):
            return 0

        # Can't bite off my head
        if bite_position >= len(self.body) - self.body_segment_density:
            return 0

        # tails_lost = bite_position // self.body_segment_density

        tails_lost = (
            1
            + (self.body_length - (len(self.body) - bite_position))
            // self.body_segment_density
        )

        if config["GAMEPLAY"]["VERZET"]:
            self.move_freeze_timer = config["GAMEPLAY"]["FREEZE_FRAMES_ON_BITTEN"]
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
        step_size = 1.0 / self.body_segment_density
        steps = int(self.speed)

        # When x or y crosses to the next grid position, we can change direction.
        # NOTE: This gives problems at higher speeds, when floating point errors.
        if self.x_pos % 1.0 == 0.0 and self.y_pos % 1.0 == 0.0:
            # Update direction
            self.move_dir_buffer = self.command
        for _ in range(steps):
            self.move_step(step_size)
            self.update_body()

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
        # math.isclose to remove floating point imprecision
        self.x_pos += round(x_pos_change, 4)
        self.y_pos += round(y_pos_change, 4)
        # print(f"Snake moved to {self.x_pos} {self.y_pos}")

    def eat_food(self, food: Food) -> bool:
        # TODO possibly should not be checked here but one place higher. This also works
        if self.head == food.pos:
            self.length += 1
            self.score += 1
            return True
        return False

    def eat_powerup(self, powerup: PowerUp) -> bool:
        if self.head == powerup.pos:
            print(f"Snake {self.name} ate powerup {powerup.name} at {powerup.pos}")
            self.apply_powerup(powerup)
            return True
        return False

    def apply_powerup(self, powerup):
        print(f"Snake {self.name} activated powerup {powerup.name} at {powerup.pos}")
        self.powerups.append(powerup)
        powerup.apply(self)

    def update_powerups(self):
        expired_powerups = []
        for powerup in self.powerups:
            powerup.update()
            if powerup.is_expired():
                expired_powerups.append(powerup)
        self.remove_powerups(expired_powerups)

    def remove_powerups(self, expired_powerups):
        for powerup in expired_powerups:
            self.powerups.remove(powerup)
            powerup.remove(self)

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

    def respawn(
        self, x_pos=None, y_pos=None, punishment=config["PLAYER"]["DEATH_PUNISHMENT"]
    ):
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
        self.body = [(x_pos, y_pos)] * self.body_length

    def report(self):
        print(f"Snake report: {self.name}")
        print(
            f"    {self.score = }\n   {self.length = }\n  {self.tails_lost = }\n  {self.tails_eaten = }"
        )
