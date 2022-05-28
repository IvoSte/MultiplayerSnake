from menus.baseMenu import BaseMenu
from viewer.colors import Color


class MainMenu(BaseMenu):
    def __init__(self, game):
        BaseMenu.__init__(self, game)
        self.name = "StartMenu"
        self.state = "start"
        self.states = [
            "start",
            "options",
            "credits",
            "quit",
        ]  # Singleplayer, multiplayer, online, offline
        self.menu_functions = {
            "start": self.start_function,
            "options": self.options_function,
            "credits": self.credits_function,
            "quit": self.quit_function,
        }

    def start_function(self):
        self.quit_menu()

    def options_function(self):
        self.quit_menu()
        self.game.options_menu()

    def credits_function(self):
        self.quit_menu()
        # self.game.show_credits()
        # TODO make credits screen.

    def quit_function(self):
        self.quit_menu()
        self.game.quit_game()
