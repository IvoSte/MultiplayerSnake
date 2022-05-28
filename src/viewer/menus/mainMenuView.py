from viewer.colors import Color
from .baseMenuView import BaseMenuView, OptionText, Cursor


class MainMenuView(BaseMenuView):
    def __init__(self, viewer, menu):
        self.viewer = viewer
        self.menu = menu
        self.display_size = self.viewer.display_size
        self.options = {
            "start": OptionText("Start Game", Color.WHITE.value, 0.5, 0.4),
            "options": OptionText("Options", Color.WHITE.value, 0.5, 0.5),
            "credits": OptionText("Credits", Color.WHITE.value, 0.5, 0.6),
            "quit": OptionText("Quit", Color.WHITE.value, 0.5, 0.7),
        }
        self.cursor = Cursor("*", Color.WHITE.value, 0.0, 0.0, -0.05, 0.01)
