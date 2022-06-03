from menus.baseMenu import BaseMenu, MenuOption
from viewer.colors import Color


class MainMenu(BaseMenu):
    def __init__(self, game):
        BaseMenu.__init__(self, game)
        self.name = "MainMenu"
        self.options = {
            "start": MenuOption("start", function=self.start_function),
            "options": MenuOption("options", function=self.options_function),
            "credits": MenuOption("credits", function=self.credits_function),
            "quit": MenuOption("quit", function=self.quit_function),
        }
        self.selected_option = self.options["start"]

    def start_function(self):
        self.quit_menu()

    def options_function(self):
        self.quit_menu()
        self.game.menuHandler.options_menu()

    def credits_function(self):
        self.quit_menu()
        # self.game.menuHandler.show_credits()
        # TODO make credits screen.

    def quit_function(self):
        self.quit_menu()
        self.game.quit_game()
