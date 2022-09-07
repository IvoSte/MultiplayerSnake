from menus.baseMenu import BaseMenu
from controls.input_controls import Controls, menu_controls, general_controls
from menus.baseMenu import OptionValueBool, MenuOption
from game.event_manager import PlayerMultiplayerEvent
from networking.network_commands import PlayerReadyCommand, PlayerUnreadyCommand
from entities.player import Player  # TODO remove this import


class MultiplayerLoadMenu(BaseMenu):
    def __init__(self, game, evManager):
        BaseMenu.__init__(self, game)
        self.name = "MultiplayerLoadMenu"
        self.connected_players = game.model.connected_player_ids
        self.options = {
            "ready check": MenuOption(
                "ready check",
                optionValue=OptionValueBool(False),
                function=self.set_player_ready,
            )
        }
        self.selected_option = self.options["ready check"]
        self.evManager = evManager

    def set_player_ready(self):
        if self.options["ready check"].optionValue.value:
            # TODO The player name needs to be sent, more than one player needs to be able to ready and it should be player dependent
            self.evManager.Post(PlayerMultiplayerEvent(command=PlayerReadyCommand()))
            ## Contact the client or send something to the client here
            self.quit_menu()
        else:
            print("Sending player unready command to server")
            self.evManager.Post(PlayerMultiplayerEvent(command=PlayerUnreadyCommand()))
            ## Send the command to the client here.
            self.quit_menu()
