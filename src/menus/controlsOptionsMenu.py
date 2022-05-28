from viewer.colors import Color
from controls.input_controls import Controls, menu_controls, general_controls
from menus.baseMenu import BaseMenu


class ControlsOptionsMenu(BaseMenu):
    def __init__(self, game):
        BaseMenu.__init__(self, game)
        self.name = "ControlsOptionsMenu"
        self.state = "rebind controls"
        self.states = ["rebind controls"]
        self.menu_functions = {
            "rebind controls": self.rebind_controls_function,
        }

    def rebind_controls_function(self):
        pass
