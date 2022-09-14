from menus.baseMenu import BaseMenu
from controls.input_controls import Controls, menu_controls, general_controls
from menus.baseMenu import OptionValueBool, MenuOption
from game.event_manager import PlayerMultiplayerEvent
from networking.network_commands import (
    PlayerReadyCommand,
    PlayerUnreadyCommand,
    CreateRoomCommand,
    JoinRoomCommand,
)
from entities.player import Player  # TODO remove this import


class MultiplayerLoadMenu(BaseMenu):
    def __init__(self, game, evManager):
        BaseMenu.__init__(self, game)
        self.name = "MultiplayerLoadMenu"
        self.options = {
            "create room": MenuOption(
                "create room",
                function=self.create_room,
            ),
            "join room": MenuOption(
                "join room",
                function=self.join_room,
            ),
        }
        self.selected_option = self.options["create room"]
        self.evManager = evManager

    def create_room(self):
        print("creating room")
        self.evManager.Post(
            PlayerMultiplayerEvent(
                command=CreateRoomCommand(self.game.model.players[0].to_json())
            )
        )

    def join_room(self):
        # TODO read player input for room code
        room_code = "AAAA"
        print("Joining room")
        self.evManager.Post(
            PlayerMultiplayerEvent(
                command=JoinRoomCommand(room_code, self.game.model.players[0].to_json())
            )
        )
