from dataclasses import dataclass
from viewer.colors import Color


class BaseMenuView:
    def __init__(self, viewer, menu):
        self.viewer = viewer
        self.menu = menu
        self.display_size = self.viewer.display_size
        self.options = {}
        self.option_values = {}
        self.cursor = Cursor()

    def draw(self):
        self.draw_options()
        # self.draw_option_values()
        self.draw_cursor()

    def draw_options(self):
        for option in self.options.values():
            self.viewer.draw_text(option.text, option.color, option.x_pos, option.y_pos)

    def draw_option_values(self):
        for option_value in self.option_values.values():
            if isinstance(option_value, OptionValueBool):
                self.viewer.draw_option_value_bool(option_value)

            if isinstance(option_value, OptionValueInt):
                self.viewer.draw_option_value_int(option_value)

            if isinstance(option_value, OptionValueList):
                self.viewer.draw_option_value_list(option_value)

    def draw_cursor(self):
        self.cursor.x_pos = self.options[self.menu.state].x_pos + self.cursor.x_offset
        self.cursor.y_pos = self.options[self.menu.state].y_pos + self.cursor.y_offset
        self.viewer.draw_text(
            self.cursor.sign, self.cursor.color, self.cursor.x_pos, self.cursor.y_pos
        )


# Text of the option, the thing being selected
@dataclass
class OptionText:
    text: str
    color: tuple
    x_pos: float
    y_pos: float


# Option values are the setting for the option,
# e.g. a boolean toggle (mute music true/false), an int value or list of options
@dataclass
class OptionValueBool:
    value: bool


@dataclass
class OptionValueInt:
    value: int
    min_value: int
    max_value: int


@dataclass
class OptionValueList:
    value: list
    index: int


# Cursor indicating currently selected option
@dataclass
class Cursor:
    sign: str = "*"
    color: tuple = Color.WHITE.value
    x_pos: float = 0.0
    y_pos: float = 0.0
    x_offset: float = -0.05
    y_offset: float = 0.01
