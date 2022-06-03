from controls.input_controls import Controls, general_controls, menu_controls
from menus.baseMenu import BaseMenu, MenuOption
from viewer.colors import Color


class PostGameMenu(BaseMenu):
    def __init__(self, game):
        BaseMenu.__init__(self, game)
        self.name = "PostGameMenu"
        self.options = {
            "restart": MenuOption("restart", function=self.restart_function),
            "options": MenuOption("options", function=self.options_function),
            "quit": MenuOption("quit", function=self.quit_function),
        }
        self.selected_option = self.options["restart"]

    def restart_function(self):
        self.quit_menu()
        self.game.menuHandler.restart_game()

    def options_function(self):
        self.quit_menu()
        self.game.menuHandler.options_menu()

    def quit_function(self):
        self.quit_menu()
        self.game.quit_game()
