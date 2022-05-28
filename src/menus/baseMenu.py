import pygame
from game.event_manager import MenuControlInputEvent
from game.event_manager import QuitEvent, RestartGameEvent
from viewer.colors import Color
from controls.input_controls import Controls, general_controls, menu_controls


class BaseMenu:
    def __init__(self, game):
        self.name = "BaseMenu"
        self.game = game
        self.state = ""
        self.states = [""]
        self.enable_menu()

    # class to override
    def menu_control(self, command):
        if command == Controls.QUIT:
            self.quit_menu()
        elif command == Controls.CONFIRM:
            self.confirm_option()
        elif command == Controls.RESTART:
            self.game.evManager.Post(RestartGameEvent)
        elif command == Controls.OPTIONS:
            print("OPTIONS menu option")

        elif command == Controls.UP:
            self.move_cursor(command)
        elif command == Controls.DOWN:
            self.move_cursor(command)
        elif command == Controls.LEFT:
            self.change_option_value(command)
        elif command == Controls.RIGHT:
            self.change_option_value(command)

    def enable_menu(self):
        self.game.state.in_menu = True
        self.game.state.in_game = False

    def quit_menu(self):
        self.game.current_menu = None
        self.game.state.in_menu = False
        self.game.state.in_game = True

    # function to override
    def confirm_option(self):
        self.menu_functions[self.state]()

    def move_cursor(self, direction):
        if direction == Controls.UP:
            self.state = self.states[(self.states.index(self.state) - 1)]
            # TODO add MaartenFX sound
        if direction == Controls.DOWN:
            self.state = self.states[
                (self.states.index(self.state) + 1) % len(self.states)
            ]
        # TODO add MaartenFX sound

    def change_option_value(self, direction):
        # Change the value of an option up or down (e.g. sound volume in the range [0-10])
        if direction == Controls.LEFT:
            print("TODO Decrease option value")
            pass
        if direction == Controls.RIGHT:
            print("TODO Increase option value")
            pass
