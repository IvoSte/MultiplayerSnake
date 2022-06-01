from viewer.colors import Color
from .baseMenuView import BaseMenuView, OptionText, Cursor


class SoundOptionsMenuView(BaseMenuView):
    def __init__(self, viewer, menu):
        BaseMenuView.__init__(self, viewer, menu)
        self.options = {
            "mute music": OptionText("Mute Music", Color.WHITE.value, 0.5, 0.4),
            "mute effects": OptionText("Mute Effects", Color.WHITE.value, 0.5, 0.5),
            "master volume": OptionText("Mastet Volume", Color.WHITE.value, 0.5, 0.6),
            "music volume": OptionText("Music Volume", Color.WHITE.value, 0.5, 0.7),
            "effects volume": OptionText("Effects Volume", Color.WHITE.value, 0.5, 0.8),
        }
        self.cursor = Cursor("*", Color.WHITE.value, 0.0, 0.0, -0.05, 0.01)
