from viewer.colors import Color
from .baseMenuView import BaseMenuView, OptionText, Cursor, MenuOptionView


class SoundOptionsMenuView(BaseMenuView):
    def __init__(self, viewer, menu):
        BaseMenuView.__init__(self, viewer, menu)
        self.options = {
            "master volume": MenuOptionView(
                menu.options["master volume"],
                "Master Volume",
                Color.WHITE.value,
                0.5,
                0.4,
                Color.WHITE.value,
            ),
            "music volume": MenuOptionView(
                menu.options["music volume"],
                "Music Volume",
                Color.WHITE.value,
                0.5,
                0.5,
                Color.WHITE.value,
            ),
            "effects volume": MenuOptionView(
                menu.options["effects volume"],
                "Effects Volume",
                Color.WHITE.value,
                0.5,
                0.6,
                Color.WHITE.value,
            ),
            "mute music": MenuOptionView(
                menu.options["mute music"],
                "Mute Music",
                Color.WHITE.value,
                0.5,
                0.7,
                Color.WHITE.value,
            ),
            "mute effects": MenuOptionView(
                menu.options["mute effects"],
                "Mute Effects",
                Color.WHITE.value,
                0.5,
                0.8,
                Color.WHITE.value,
            ),
        }
