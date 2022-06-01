from viewer.colors import Color
from controls.input_controls import Controls, menu_controls, general_controls
from menus.baseMenu import BaseMenu, MenuOption


class ControlsOptionsMenu(BaseMenu):
    def __init__(self, game):
        BaseMenu.__init__(self, game)
        self.name = "ControlsOptionsMenu"
        self.options = {
            "rebind controls": MenuOption(
                "rebind controls", function=self.rebind_controls_function
            )
        }
        self.selected_option = self.options["rebind controls"]

    def rebind_controls_function(self):
        pass
