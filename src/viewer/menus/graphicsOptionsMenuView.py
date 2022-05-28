from viewer.colors import Color
from .baseMenuView import BaseMenuView, OptionText, Cursor


class GraphicsOptionsMenuView(BaseMenuView):
    def __init__(self, viewer, menu):
        self.viewer = viewer
        self.menu = menu
        self.display_size = self.viewer.display_size
        self.options = {
            "resolution": OptionText("Resolution", Color.WHITE.value, 0.5, 0.4),
            "background visuals": OptionText(
                "Background Visuals", Color.WHITE.value, 0.5, 0.5
            ),
        }
        self.cursor = Cursor("*", Color.WHITE.value, 0.0, 0.0, -0.05, 0.01)
