from viewer.colors import Color
from .baseMenuView import BaseMenuView, Cursor, MenuOptionView


class GraphicsOptionsMenuView(BaseMenuView):
    def __init__(self, viewer, menu):
        BaseMenuView.__init__(self, viewer, menu)
        self.options = {
            "resolution": MenuOptionView(
                menu.options["resolution"],
                "Resolution",
                Color.WHITE.value,
                0.5,
                0.4,
                Color.WHITE.value,
            ),
            "background visuals": MenuOptionView(
                menu.options["background visuals"],
                "Background Visuals",
                Color.WHITE.value,
                0.5,
                0.5,
                Color.WHITE.value,
            ),
        }
