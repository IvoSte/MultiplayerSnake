from viewer.colors import Color
from controls.input_controls import Controls, menu_controls, general_controls
from menus.baseMenu import BaseMenu


class GraphicsOptionsMenu(BaseMenu):
    def __init__(self, game):
        BaseMenu.__init__(self, game)
        self.name = "GraphicsOptionsMenu"
        self.state = "resolution"
        self.states = ["resolution", "background visuals"]
        self.menu_functions = {
            "resolution": self.set_resolution_function,
            "background visuals": self.set_background_visuals_function,
        }

    def set_resolution_function(self):
        pass

    def set_background_visuals_function(self):
        pass
