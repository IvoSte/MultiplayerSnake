from viewer.colors import Color
from .baseMenuView import BaseMenuView, OptionText, Cursor, MenuOptionView


class ControlsOptionsMenuView(BaseMenuView):
    def __init__(self, viewer, menu):
        BaseMenuView.__init__(self, viewer, menu)
        self.options = {
            "rebind controls": MenuOptionView(
                menu.options["rebind controls"],
                "Rebind Controls",
                Color.WHITE.value,
                0.5,
                0.4,
                Color.WHITE.value,
            ),
        }
