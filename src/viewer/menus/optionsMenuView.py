from viewer.colors import Color
from .baseMenuView import BaseMenuView, OptionText, Cursor


class OptionsMenuView(BaseMenuView):
    def __init__(self, viewer, menu):
        self.viewer = viewer
        self.menu = menu
        self.display_size = self.viewer.display_size
        self.options = {
            "gameplay": OptionText("Gameplay", Color.WHITE.value, 0.5, 0.4),
            "graphics": OptionText("Graphics", Color.WHITE.value, 0.5, 0.5),
            "sound": OptionText("Sound", Color.WHITE.value, 0.5, 0.6),
            "controls": OptionText("Controls", Color.WHITE.value, 0.5, 0.7),
        }
        self.cursor = Cursor("*", Color.WHITE.value, 0.0, 0.0, -0.05, 0.01)
