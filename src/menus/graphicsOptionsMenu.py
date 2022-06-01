from viewer.colors import Color
from controls.input_controls import Controls, menu_controls, general_controls
from menus.baseMenu import BaseMenu, MenuOption


class GraphicsOptionsMenu(BaseMenu):
    def __init__(self, game):
        BaseMenu.__init__(self, game)
        self.name = "GraphicsOptionsMenu"
        self.options = {
            "resolution": MenuOption(
                "resolution", function=self.set_resolution_function
            ),
            "background visuals": MenuOption(
                "background visuals", function=self.set_background_visuals_function
            ),
        }
        self.selected_option = self.options["resolution"]

    def set_resolution_function(self):
        pass

    def set_background_visuals_function(self):
        pass
