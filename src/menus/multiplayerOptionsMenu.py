from menus.baseMenu import BaseMenu
from menus.baseMenu import OptionValueBool, OptionValueInt, MenuOption
from game.config import config


class MultiplayerOptionsMenu(BaseMenu):
    def __init__(self, game):
        BaseMenu.__init__(self, game)
        self.name = "MultiplayerOptionsMenu"
        self.options = {
            "grid size x": MenuOption(
                "grid size x",
                optionValue=OptionValueInt(config["GAME"]["GRID_SIZE_X"], 5, 10, 100),
                function=self.set_grid_size_x,
            ),
            "grid size y": MenuOption(
                "grid size y",
                optionValue=OptionValueInt(config["GAME"]["GRID_SIZE_Y"], 5, 10, 100),
                function=self.set_grid_size_y,
            ),
        }
        self.selected_option = self.options["grid size x"]

    def set_grid_size_x(self):
        new_value = self.options["grid size x"].optionValue.value
        config["GAME"]["GRID_SIZE_X"] = new_value

    def set_grid_size_y(self):
        new_value = self.options["grid size y"].optionValue.value
        config["GAME"]["GRID_SIZE_Y"] = new_value
