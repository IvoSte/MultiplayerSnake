from enum import Enum
from env_variables import CONTROLLER_DEADZONE
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

def controllerInputHandler(event):
    deadzone = CONTROLLER_DEADZONE
    if event.type == pygame.JOYAXISMOTION:
        value = event.value
        if event.axis == 0:
            if abs(value) >= deadzone:
                if value < 0:
                    return Controls.LEFT
                else:
                    return Controls.RIGHT

        elif event.axis == 1:
            if abs(value) >= deadzone:
                if value < 0:
                    return Controls.UP
                else:
                    return Controls.DOWN

    if event.type == pygame.JOYHATMOTION:
        x,y = event.value
        if x == -1:
            return Controls.LEFT
        if x == 1:
            return Controls.RIGHT
        if y == 1:
            return Controls.UP
        if y == -1:
            return Controls.DOWN





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
    pygame.K_UP: Controls.UP,
    pygame.K_LEFT: Controls.LEFT,
    pygame.K_DOWN: Controls.DOWN,
    pygame.K_RIGHT: Controls.RIGHT,
}

player_2_controls = {
    pygame.K_w: Controls.UP,
    pygame.K_a: Controls.LEFT,
    pygame.K_s: Controls.DOWN,
    pygame.K_d: Controls.RIGHT,
}

player_3_controls = {
    pygame.K_t: Controls.UP,
    pygame.K_f: Controls.LEFT,
    pygame.K_g: Controls.DOWN,
    pygame.K_h: Controls.RIGHT,
}

player_4_controls = {
    pygame.K_i: Controls.UP,
    pygame.K_j: Controls.LEFT,
    pygame.K_k: Controls.DOWN,
    pygame.K_l: Controls.RIGHT,
}
