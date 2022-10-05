from menus.baseMenu import OptionValueBool, OptionValueInt, MenuOption
from game.config import config
from viewer.colors import Color
from controls.input_controls import Controls, menu_controls, general_controls
from menus.baseMenu import BaseMenu
from game.config import config

class GameplayOptionsMenu(BaseMenu):
    def __init__(self, game):
        BaseMenu.__init__(self, game)
        self.name = "GameplayOptionsMenu"
        self.options = {
            "players": MenuOption(
                "players",
                optionValue=OptionValueInt(
                    config['PLAYER']['NUMBER_OF_PLAYERS'], 1, 1, 4),
                function=self.set_players_function,
            ),
            "time limit": MenuOption(
                "time limit",
                optionValue=OptionValueInt(
                    config['GAMEPLAY']['GAME_TIMER'], 5, 5, 90),
                function=self.set_time_limit_function,
            ),
            "countdown": MenuOption(
                "countdown",
                optionValue=OptionValueInt(
                    config['GAMEPLAY']['START_COUNTDOWN'], 1, 0, 5),
                function=self.set_countdown_function,
            ),
            "tail biting": MenuOption(
                "tail biting",
                optionValue=OptionValueBool(config['MODE']['TAIL_BITING']),
                function=self.set_tail_biting_function,
            ),
            "tail stealing": MenuOption(
                "tail stealing",
                optionValue=OptionValueBool(config['MODE']['TAIL_STEALING']),
                function=self.set_tail_stealing_function,
            ),
            "snake speed": MenuOption(
                "snake speed",
                optionValue=OptionValueInt(
                    config['PLAYER']['SNAKE_SPEED'], 1, 1, 6),
                function=self.set_snake_speed_function,
            ),
        }
        self.selected_option = self.options["players"]

    def set_players_function(self):
        new_value = self.options["players"].optionValue.value
        config['PLAYER']['NUMBER_OF_PLAYERS'] = new_value

    def set_time_limit_function(self):
        new_value = self.options["time limit"].optionValue.value
        config['GAMEPLAY']['GAME_TIMER'] = new_value
        # Set the timer switch to false if the timer is set to 0, and to true for positive values.
        config['GAMEPLAY']['GAME_TIMER_SWITCH'] = bool(new_value)

    def set_countdown_function(self):
        new_value = self.options["countdown"].optionValue.value
        config['GAMEPLAY']['START_COUNTDOWN'] = new_value

    def set_tail_biting_function(self):
        new_value = self.options["tail biting"].optionValue.value
        config['MODE']['TAIL_BITING'] = new_value

    def set_tail_stealing_function(self):
        new_value = self.options["tail stealing"].optionValue.value
        config['MODE']['TAIL_STEALING'] = new_value

    def set_snake_speed_function(self):
        new_value = self.options["snake speed"].optionValue.value
        config['PLAYER']['SNAKE_SPEED'] = new_value
