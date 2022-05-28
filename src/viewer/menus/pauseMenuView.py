from viewer.colors import Color
from .baseMenuView import BaseMenuView, OptionText, Cursor


class PauseMenuView(BaseMenuView):
    def __init__(self, viewer, menu):
        self.viewer = viewer
        self.menu = menu
        self.display_size = self.viewer.display_size
        self.options = {
            "unpause": OptionText("Unpause", Color.WHITE.value, 0.5, 0.4),
            "restart": OptionText("Restart", Color.WHITE.value, 0.5, 0.5),
            "options": OptionText("Options", Color.WHITE.value, 0.5, 0.6),
            "quit": OptionText("Quit", Color.WHITE.value, 0.5, 0.7),
        }
        self.cursor = Cursor("*", Color.WHITE.value, 0.0, 0.0, -0.05, 0.01)