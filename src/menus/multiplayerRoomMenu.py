from menus.baseMenu import BaseMenu
from controls.input_controls import Controls, menu_controls, general_controls
from menus.baseMenu import OptionValueBool, MenuOption
from game.event_manager import PlayerMultiplayerEvent
from networking.network_commands import (
    PlayerReadyCommand,
    PlayerUnreadyCommand,
    CreateRoomCommand,
    StartGameCommand,
    LeaveRoomCommand,
)


class MultiplayerRoomMenu(BaseMenu):
    def __init__(self, game, evManager):
        BaseMenu.__init__(self, game)
        self.name = "MultiplayerRoomMenu"
        # self.connected_players = {
        #     PLAYER_ID: {
        #         "name": "",
        #         "color": "",
        #         "ready_status": False,
        #     }
        # }
        self.connected_players = {}
        self.room_code = self.game.model.room_code
        self.options = {
            "ready check": MenuOption(
                "ready check",
                optionValue=OptionValueBool(False),
                function=self.set_player_ready,
            ),
            "start game": MenuOption(
                "start game",
                function=self.start_game,
            ),
            "multiplayer options": MenuOption(
                "multiplayer options",
                function=self.multiplayer_options,
            ),
        }
        self.selected_option = self.options["ready check"]
        self.evManager = evManager

    def set_player_ready(self):
        if self.options["ready check"].optionValue.value:
            # TODO The player name needs to be sent, more than one player needs to be able to ready and it should be player dependent
            self.evManager.Post(
                PlayerMultiplayerEvent(
                    command=PlayerReadyCommand(
                        self.room_code, self.game.model.players[0].name
                    )
                )
            )
            ## Contact the client or send something to the client here
        else:
            self.evManager.Post(
                PlayerMultiplayerEvent(
                    command=PlayerUnreadyCommand(
                        self.room_code, self.game.model.players[0].name
                    )
                )
            )
            ## Send the command to the client here.

    def start_game(self):
        self.evManager.Post(
            PlayerMultiplayerEvent(command=StartGameCommand(self.room_code))
        )
        # send message to server to check if all connected players are ready
        # receive reply yes or no
        # if yes, send start game command
        # if no, do nothing or send error

    def multiplayer_options(self):
        self.quit_menu()
        self.game.menuHandler.multiplayer_options_menu()

    def set_connected_players(self):
        self.connected_players = self.game.model.connected_player_ids

    def leave_room(self):
        self.evManager.Post(
            PlayerMultiplayerEvent(command=LeaveRoomCommand(self.room_code))
        )

    def quit_menu(self):
        self.leave_room()
        self.game.menuHandler.quit_menu()

    def back_menu(self):
        self.leave_room()
        self.game.menuHandler.back_menu()
