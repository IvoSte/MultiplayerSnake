from menus.baseMenu import BaseMenu
from controls.input_controls import Controls, menu_controls, general_controls
from menus.baseMenu import OptionValueBool, MenuOption


class MultiplayerLoadMenu(BaseMenu):
    def __init__(self, game):
        BaseMenu.__init__(self, game)
        self.name = "MultiplayerLoadMenu"
        self.options = {
            "ready check": MenuOption(
                "ready check",
                optionValue=OptionValueBool(False),
                function=self.set_player_ready,
            )
        }
        self.selected_option = self.options["ready check"]

    def set_player_ready(self):
        if self.options["ready check"].optionValue.value:
            print("Sending player ready command to server")
            ## Contact the client or send something to the client here
            self.quit_menu()
        else:
            print("Sending player unready command to server")
            ## Send the command to the client here.
            self.quit_menu()
