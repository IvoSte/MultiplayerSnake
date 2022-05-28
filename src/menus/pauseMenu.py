from controls.input_controls import Controls, general_controls, menu_controls
from menus.baseMenu import BaseMenu
from viewer.colors import Color


class PauseMenu(BaseMenu):
    def __init__(self, game):
        BaseMenu.__init__(self, game)
        self.name = "PauseMenu"
        self.state = "unpause"
        self.states = ["unpause", "restart", "options", "quit"]
        self.menu_functions = {
            "unpause": self.unpause_function,
            "restart": self.restart_function,
            "options": self.options_function,
            "quit": self.quit_function,
        }

    def unpause_function(self):
        self.quit_menu()

    def restart_function(self):
        self.quit_menu()
        self.game.restart_game()

    def options_function(self):
        self.quit_menu()
        self.game.options_menu()

    def quit_function(self):
        self.quit_menu()
        self.game.quit_game()


# when a menu is entered, it is created in game as Menu. Then, in viewer, viewer knows game is
# in a menu, and checks the menu's name, which is the key in a dict in viewer, pointing to
# the equally named MenuView object, which has its own draw function.
# Menus created in game are removed when they are exited (so they dont keep listening to events)
# All menu view objects can be created at init, and kept alive to be called. Or, just place a static
# version of the class in the dict, so a new one is instantiated too.