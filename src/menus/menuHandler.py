from menus.controlsOptionsMenu import ControlsOptionsMenu
from menus.gameplayOptionsMenu import GameplayOptionsMenu
from menus.graphicsOptionsMenu import GraphicsOptionsMenu
from menus.soundOptionsMenu import SoundOptionsMenu
from menus.optionsMenu import OptionsMenu
from menus.pauseMenu import PauseMenu
from menus.postGameMenu import PostGameMenu


class MenuHandler:
    def __init__(self, game):
        self.game = game
        self.menu_stack = []  # so you don't quit out of all menus but you can traverse
        self.current_menu = None

    def postgame_menu(self):
        self.current_menu = PostGameMenu(self.game)

    def pause_menu(self):
        self.current_menu = PauseMenu(self.game)

    def options_menu(self):
        self.current_menu = OptionsMenu(self.game)

    def gameplay_options_menu(self):
        self.current_menu = GameplayOptionsMenu(self.game)

    def graphics_options_menu(self):
        self.current_menu = GraphicsOptionsMenu(self.game)

    def sound_options_menu(self):
        self.current_menu = SoundOptionsMenu(self.game)

    def controls_options_menu(self):
        self.current_menu = ControlsOptionsMenu(self.game)
