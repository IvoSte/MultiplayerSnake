from dataclasses import dataclass
from viewer.colors import Color


class BaseMenuView:
    def __init__(self, viewer, menu):
        self.viewer = viewer
        self.menu = menu
        self.display_size = self.viewer.display_size
        self.options = {}
        self.cursor = Cursor()

    def draw(self):
        self.draw_options()
        self.draw_cursor()

    def draw_options(self):
        for option in self.options.values():
            self.viewer.draw_text(option.text, option.color, option.x_pos, option.y_pos)

    def draw_cursor(self):
        self.cursor.x_pos = self.options[self.menu.state].x_pos + self.cursor.x_offset
        self.cursor.y_pos = self.options[self.menu.state].y_pos + self.cursor.y_offset
        self.viewer.draw_text(
            self.cursor.sign, self.cursor.color, self.cursor.x_pos, self.cursor.y_pos
        )


@dataclass
class OptionText:
    text: str
    color: tuple
    x_pos: float
    y_pos: float


@dataclass
class Cursor:
    sign: str = "*"
    color: tuple = Color.WHITE.value
    x_pos: float = 0.0
    y_pos: float = 0.0
    x_offset: float = -0.05
    y_offset: float = 0.01