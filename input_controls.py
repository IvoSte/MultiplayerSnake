from enum import Enum
import pygame

class Controls(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    QUIT = 4
    CONFIRM = 5
    RESTART = 6

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
    elif command.key == pygame.K_Q:
        return Controls.QUIT
    elif command.key == pygame.K_C:
        return Controls.CONFIRM
    elif command.key == pygame.K_R:
        return Controls.RESTART
    else :
        return None
