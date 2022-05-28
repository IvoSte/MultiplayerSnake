from viewer.colors import Color
from controls.input_controls import Controls, menu_controls, general_controls
from menus.baseMenu import BaseMenu


class OptionsMenu(BaseMenu):
    def __init__(self, game):
        BaseMenu.__init__(self, game)
        self.name = "OptionsMenu"
        self.state = "gameplay"
        self.states = ["gameplay", "graphics", "sound", "controls"]
        self.menu_functions = {
            "gameplay": self.gameplay_function,
            "graphics": self.graphics_function,
            "sound": self.sound_function,
            "controls": self.controls_function,
        }

    def gameplay_function(self):
        self.quit_menu()
        self.game.gameplay_options_menu()

    def graphics_function(self):
        self.quit_menu()
        self.game.graphics_options_menu()

    def sound_function(self):
        self.quit_menu()
        self.game.sound_options_menu()

    def controls_function(self):
        self.quit_menu()
        self.game.controls_options_menu()
