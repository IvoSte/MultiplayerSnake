from .baseMenuView import BaseMenuView, MenuOptionView, TextView
from viewer.colors import Color


class MultiplayerRoomMenuView(BaseMenuView):
    def __init__(self, viewer, menu):
        BaseMenuView.__init__(self, viewer, menu)
        self.text = {
            "connected players:": TextView(
                "connected players", Color.WHITE.value, 0.45, 0.6
            ),
            "room code:": TextView("room code", Color.WHITE.value, 0.45, 0.3),
            "ROOM_CODE": TextView(self.menu.room_code, Color.WHITE.value, 0.7, 0.3),
        }

        self.menu.set_connected_players()  # TODO Dirty, please check if there is another way

        for idx, player in enumerate(menu.connected_players):
            self.text[player["name"]] = TextView(
                player["name"], Color.WHITE.value, 0.5, 0.6 + (0.05 * (idx + 1))
            )
            self.text[player["name"] + "_is_ready"] = TextView(
                player["is_ready"], Color.WHITE.value, 0.6, 0.6 + (0.05 * (idx + 1))
            )

        self.options = {
            "ready check": MenuOptionView(
                menu.options["ready check"],
                "Ready?",
                Color.WHITE.value,
                0.5,
                0.4,
                Color.WHITE.value,
            ),
            "start game": MenuOptionView(
                menu.options["start game"],
                "Start Game",
                Color.WHITE.value,
                0.5,
                0.45,
                Color.WHITE.value,
            ),
        }
