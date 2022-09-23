from menus.controlsOptionsMenu import ControlsOptionsMenu
from menus.gameplayOptionsMenu import GameplayOptionsMenu
from menus.graphicsOptionsMenu import GraphicsOptionsMenu
from menus.soundOptionsMenu import SoundOptionsMenu
from menus.optionsMenu import OptionsMenu
from menus.pauseMenu import PauseMenu
from menus.postGameMenu import PostGameMenu
from menus.multiplayerLoadMenu import MultiplayerLoadMenu
from menus.mainMenu import MainMenu
from menus.multiplayerRoomMenu import MultiplayerRoomMenu


class MenuHandler:
    def __init__(self, game, evManager):
        self.game = game
        self.evManager = evManager
        self.menu_stack = []  # so you don't quit out of all menus but you can traverse
        self.current_menu = None

    def quit_menu(self):
        self.current_menu = None
        self.game.state.in_menu = False
        self.game.state.in_game = True

    def main_menu(self):
        self.current_menu = MainMenu(self.game)

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

    def multiplayer_menu(self):
        self.current_menu = MultiplayerLoadMenu(self.game, self.evManager)

    def multiplayer_room_menu(self):
        self.current_menu = MultiplayerRoomMenu(self.game, self.evManager)
