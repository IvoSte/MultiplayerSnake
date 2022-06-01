from dataclasses import dataclass
from menus.baseMenu import MenuOption
from menus.baseMenu import OptionValueBool, OptionValueInt, OptionValueList
from viewer.colors import Color


class BaseMenuView:
    def __init__(self, viewer, menu):
        self.viewer = viewer
        self.menu = menu
        self.display_size = self.viewer.display_size
        self.options: dict[str, MenuOptionView]  # Dict of options
        self.cursor = Cursor("➜", Color.WHITE.value, 0.0, 0.0, -0.05, 0.01)

    def draw(self):
        self.draw_options()
        self.draw_option_values()
        self.draw_cursor()

    def draw_options(self):
        for option_view in self.options.values():
            self.viewer.draw_text(
                option_view.text,
                option_view.text_color,
                option_view.x_pos,
                option_view.y_pos,
            )

    def draw_option_values(self):
        for option_view in self.options.values():
            if option_view.option.optionValue != None:
                self.draw_option_value(option_view)

    def draw_option_value(self, option_view):
        self.viewer.draw_text(
            str(option_view.option.optionValue.value),
            option_view.value_color,
            option_view.x_pos + option_view.value_x_offset,
            option_view.y_pos + option_view.value_y_offset,
        )

    def draw_cursor(self):
        self.cursor.x_pos = (
            self.options[self.menu.selected_option.name].x_pos + self.cursor.x_offset
        )
        self.cursor.y_pos = (
            self.options[self.menu.selected_option.name].y_pos + self.cursor.y_offset
        )
        self.viewer.draw_text(
            self.cursor.sign, self.cursor.color, self.cursor.x_pos, self.cursor.y_pos
        )


@dataclass
class MenuOptionView:
    option: MenuOption
    text: str
    text_color: tuple
    x_pos: float
    y_pos: float
    value_color: tuple
    value_x_offset: float = 0.3
    value_y_offset: float = 0.0


# Text of the option, the thing being selected
# DEPRECIATED
@dataclass
class OptionText:
    text: str
    color: tuple
    x_pos: float
    y_pos: float


# Option value to be displayed. Later include more drawing options (like arrows and such)
# DEPRECIATED
@dataclass
class OptionValueView:
    color: tuple
    x_offset: float = 0.15
    y_offset: float = 0.0


# Cursor indicating currently selected option
@dataclass
class Cursor:
    sign: str = "*"
    color: tuple = Color.WHITE.value
    x_pos: float = 0.0
    y_pos: float = 0.0
    x_offset: float = -0.05
    y_offset: float = 0.01
