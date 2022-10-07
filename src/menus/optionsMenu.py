from viewer.colors import Color
from controls.input_controls import Controls, menu_controls, general_controls
from menus.baseMenu import BaseMenu, MenuOption


class OptionsMenu(BaseMenu):
    def __init__(self, game):
        BaseMenu.__init__(self, game)
        self.name = "OptionsMenu"
        self.options = {
            "gameplay": MenuOption("gameplay", function=self.gameplay_function),
            "graphics": MenuOption("graphics", function=self.graphics_function),
            "sound": MenuOption("sound", function=self.sound_function),
            "controls": MenuOption("controls", function=self.controls_function),
        }
        self.selected_option = self.options["gameplay"]

    def gameplay_function(self):
        self.game.menuHandler.gameplay_options_menu()

    def graphics_function(self):
        self.game.menuHandler.graphics_options_menu()

    def sound_function(self):
        self.game.menuHandler.sound_options_menu()

    def controls_function(self):
        self.game.menuHandler.controls_options_menu()
