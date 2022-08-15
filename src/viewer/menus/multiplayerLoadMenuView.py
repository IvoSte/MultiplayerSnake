from .baseMenuView import BaseMenuView, MenuOptionView
from viewer.colors import Color


class MultiplayerLoadMenuView(BaseMenuView):
    def __init__(self, viewer, menu):
        BaseMenuView.__init__(self, viewer, menu)
        self.options = {
            "ready check": MenuOptionView(
                menu.options["ready check"],
                "Ready?",
                Color.WHITE.value,
                0.5,
                0.4,
                Color.WHITE.value,
            )
        }
