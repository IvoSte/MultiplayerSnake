from viewer.colors import Color
from .baseMenuView import BaseMenuView, OptionText, Cursor, MenuOptionView


class OptionsMenuView(BaseMenuView):
    def __init__(self, viewer, menu):
        BaseMenuView.__init__(self, viewer, menu)
        self.options = {
            "gameplay": MenuOptionView(
                menu.options["gameplay"],
                "Gameplay",
                Color.WHITE.value,
                0.5,
                0.4,
                Color.WHITE.value,
            ),
            "graphics": MenuOptionView(
                menu.options["graphics"],
                "Graphics",
                Color.WHITE.value,
                0.5,
                0.5,
                Color.WHITE.value,
            ),
            "sound": MenuOptionView(
                menu.options["sound"],
                "Sound",
                Color.WHITE.value,
                0.5,
                0.6,
                Color.WHITE.value,
            ),
            "controls": MenuOptionView(
                menu.options["controls"],
                "Controls",
                Color.WHITE.value,
                0.5,
                0.7,
                Color.WHITE.value,
            ),
        }
