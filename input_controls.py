from enum import Enum
import pygame

class Controls(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    QUIT = 4
    PAUSE = 5
    CONFIRM = 6
    RESTART = 7

def inputHandler(command):
    assert command.type == pygame.KEYDOWN, "Command issued to inputHandler when event type is not a keypress."
    if command.key == pygame.K_LEFT:
        return Controls.LEFT
    elif command.key == pygame.K_RIGHT:
        return Controls.RIGHT
    elif command.key == pygame.K_UP:
        return Controls.UP
    elif command.key == pygame.K_DOWN:
        return Controls.DOWN
    elif command.key == pygame.K_q:
        return Controls.QUIT
    elif command.key == pygame.K_p:
        return Controls.PAUSE
    elif command.key == pygame.K_c:
        return Controls.CONFIRM
    elif command.key == pygame.K_r:
        return Controls.RESTART
    else :
        return None

# Crude implementation, make better later
general_controls = {
    pygame.K_q: Controls.QUIT,
    pygame.K_c: Controls.CONFIRM,
    pygame.K_p: Controls.PAUSE,
    pygame.K_r: Controls.RESTART,
}

default_player_controls = {
    pygame.K_LEFT: Controls.LEFT,
    pygame.K_RIGHT: Controls.RIGHT,
    pygame.K_UP: Controls.UP,
    pygame.K_DOWN: Controls.DOWN,
}

player_1_controls = {
    pygame.K_LEFT: Controls.LEFT,
    pygame.K_RIGHT: Controls.RIGHT,
    pygame.K_UP: Controls.UP,
    pygame.K_DOWN: Controls.DOWN,
}

player_2_controls = {
    pygame.K_a: Controls.LEFT,
    pygame.K_d: Controls.RIGHT,
    pygame.K_w: Controls.UP,
    pygame.K_s: Controls.DOWN,
}