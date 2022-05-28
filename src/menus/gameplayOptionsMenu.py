from viewer.colors import Color
from controls.input_controls import Controls, menu_controls, general_controls
from menus.baseMenu import BaseMenu


class GameplayOptionsMenu(BaseMenu):
    def __init__(self, game):
        BaseMenu.__init__(self, game)
        self.name = "GameplayOptionsMenu"
        self.state = "players"
        self.states = [
            "players",
            "time limit",
            "countdown",
            "tail biting",
            "tail stealing",
            "snake speed",
        ]
        self.menu_functions = {
            "players" : self.set_players_function,
            "time limit" : self.set_time_limit_function,
            "countdown" : self.set_countdown_function,
            "tail biting" : self.set_tail_biting_function,
            "tail stealing" : self.set_tail_stealing_function,
            "snake speed" : self.set_snake_speed_function,
        }

    def set_players_function(self):
        pass

    def set_time_limit_function(self):
        pass

    def set_countdown_function(self):
        pass

    def set_tail_biting_function(self):
        pass

    def set_tail_stealing_function(self):
        pass

    def set_snake_speed_function(self):
        pass
