from controls.input_controls import Controls, general_controls, menu_controls
from menus.baseMenu import BaseMenu
from viewer.colors import Color


class PostGameMenu(BaseMenu):
    def __init__(self, game):
        BaseMenu.__init__(self, game)
        self.name = "PostGameMenu"
        self.state = "restart"
        self.states = ["restart", "options", "quit"]
        self.menu_functions = {
            "restart": self.restart_function,
            "options": self.options_function,
            "quit": self.quit_function,
        }

    def restart_function(self):
        self.quit_menu()
        self.game.restart_game()

    def options_function(self):
        self.quit_menu()
        self.game.options_menu()

    def quit_function(self):
        self.quit_menu()
        self.game.quit_game()