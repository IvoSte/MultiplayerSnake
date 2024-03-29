from viewer.colors import Color
from .baseMenuView import (
    BaseMenuView,
    Cursor,
    MenuOptionView,
)


class MultiplayerOptionsMenuView(BaseMenuView):
    def __init__(self, viewer, menu):
        BaseMenuView.__init__(self, viewer, menu)
        self.options = {
            "grid size x": MenuOptionView(
                menu.options["grid size x"],
                "Grid size X",
                Color.WHITE.value,
                0.5,
                0.4,
                Color.WHITE.value,
            ),
            "grid size y": MenuOptionView(
                menu.options["grid size y"],
                "Grid size Y",
                Color.WHITE.value,
                0.5,
                0.45,
                Color.WHITE.value,
            ),
        }
