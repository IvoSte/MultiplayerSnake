from .baseMenuView import BaseMenuView, MenuOptionView, TextView
from viewer.colors import Color


class MultiplayerLoadMenuView(BaseMenuView):
    def __init__(self, viewer, menu):
        BaseMenuView.__init__(self, viewer, menu)
        self.text = {
            "connected players:": TextView(
                "connected players", Color.WHITE.value, 0.45, 0.6
            )
        }

        self.menu.set_connected_players()  # TODO Dirty, please check if there is another way
        print(f"connected players : {menu.connected_players}")
        for idx, player in enumerate(menu.connected_players):
            self.text[player] = TextView(
                player, Color.WHITE.value, 0.5, 0.6 + (0.05 * (idx + 1))
            )

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
