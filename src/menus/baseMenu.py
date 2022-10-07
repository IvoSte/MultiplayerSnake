import pygame
from game.event_manager import MenuControlInputEvent
from game.event_manager import QuitEvent, RestartGameEvent
from viewer.colors import Color
from controls.input_controls import Controls, general_controls, menu_controls
from dataclasses import dataclass, replace
from typing import Callable


class BaseMenu:
    def __init__(self, game):
        self.name = "BaseMenu"
        self.game = game
        self.options: dict[str, MenuOption]
        self.selected_option: MenuOption
        self.enable_menu()

    def menu_control(self, command):
        if command == Controls.QUIT:
            self.quit_menu()
        elif command == Controls.BACK:
            self.back_menu()
        elif command == Controls.CONFIRM:
            self.confirm_option()
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
        self.game.menuHandler.quit_menu()

    def back_menu(self):
        self.game.menuHandler.back_menu()

    # function to override
    def confirm_option(self):
        if isinstance(self.selected_option.function, Callable):
            self.selected_option.function()

    def move_cursor(self, direction):
        if direction == Controls.UP:
            # select the next option in the dict (using lists to get indices)
            self.selected_option = list(self.options.values())[
                (list(self.options.values()).index(self.selected_option) - 1)
            ]
            # self.selected_option = self.options[(self.options.index(self.selected_option) - 1)]
            # TODO add MaartenFX sound
        if direction == Controls.DOWN:
            self.selected_option = list(self.options.values())[
                (list(self.options.values()).index(self.selected_option) + 1)
                % len(self.options)
            ]
            # self.selected_option = self.options[
            #     (self.options.index(self.selected_option) + 1) % len(self.options)
            # ]
            # TODO add MaartenFX sound

    def change_option_value(self, direction):
        # If this selected option does not have values, we can't change it.
        if self.selected_option.optionValue == None:
            return

        # print(self.selected_option.optionValue)
        # print(self.selected_option.optionValue.value)

        # Change the value of an option up or down (e.g. sound volume in the range [0-10])
        if isinstance(self.selected_option.optionValue, OptionValueBool):
            self.change_option_bool(self.selected_option.optionValue, direction)

        if isinstance(self.selected_option.optionValue, OptionValueInt):
            self.change_option_int(self.selected_option.optionValue, direction)

        if isinstance(self.selected_option.optionValue, OptionValueList):
            self.change_option_list(self.selected_option.optionValue, direction)

    def change_option_bool(self, optionValue, direction):
        # Change the value of a boolean option (e.g. tail biting true or false)
        if direction == Controls.LEFT:
            optionValue.value = True
        if direction == Controls.RIGHT:
            optionValue.value = False

    def change_option_int(self, optionValue, direction):
        # Change the value of an integer option  (e.g. number of players)
        if direction == Controls.LEFT:
            # Decrease the value or set the min
            optionValue.value = max(
                optionValue.min_value, optionValue.value - optionValue.step_size
            )
        if direction == Controls.RIGHT:
            # Increase the value or set the max
            optionValue.value = min(
                optionValue.max_value, optionValue.value + optionValue.step_size
            )

    def change_option_list(self, optionValue, direction):
        # Change the value of a list option (e.g. player colourmap)
        if direction == Controls.LEFT:
            optionValue.index = max(0, optionValue.index - 1)
        if direction == Controls.RIGHT:
            optionValue.index = min(len(optionValue.values) - 1, optionValue.index + 1)


# Option values are the setting for the option,
# e.g. a boolean toggle (mute music true/false), an int value or list of options
@dataclass
class OptionValue:
    # value: int
    pass


@dataclass
class OptionValueBool(OptionValue):
    value: bool


@dataclass
class OptionValueInt(OptionValue):
    value: int
    step_size: int
    min_value: int
    max_value: int


@dataclass
class OptionValueList(OptionValue):
    value: list
    index: int


@dataclass
class MenuOption:
    name: str
    optionValue: OptionValue = None
    function: Callable = None
