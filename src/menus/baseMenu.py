import pygame
from game.event_manager import MenuControlInputEvent
from game.event_manager import QuitEvent, RestartGameEvent
from viewer.colors import Color
from controls.input_controls import Controls, general_controls, menu_controls


class BaseMenu:
    def __init__(self, game):
        self.name = "BaseMenu"
        # self.evManager = evManager
        # self.evManager.RegisterListener(self)
        self.game = game
        self.in_menu = True
        self.state = ""
        self.states = [""]

    # def notify(self, event):
    #    if isinstance(event, MenuControlInputEvent):
    #        self.menu_control(event.command)

    def display_menu(self):
        self.in_menu = True

    # class to override
    def menu_control(self, command):
        if command == Controls.PAUSE:
            self.game.pause_menu()
        elif command == Controls.QUIT:
            self.game.evManager.Post(QuitEvent)
        elif command == Controls.CONFIRM:
            print("Confirm menu option")
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
            self.move_cursor(command)
        elif command == Controls.RIGHT:
            self.move_cursor(command)

    def quit_menu(self):
        self.in_menu = False

    # function to override
    def confirm_option(self):
        print(f"Confirming menu choice: {self.state}")
        self.menu_functions[self.state]()

    def move_cursor(self, direction):
        if direction == Controls.UP:
            self.state = self.states[(self.states.index(self.state) - 1)]
            # TODO add MaartenFX sound
        if direction == Controls.DOWN:
            self.state = self.states[
                (self.states.index(self.state) + 1) % (len(self.states) - 1)
            ]
            # TODO add MaartenFX sound
