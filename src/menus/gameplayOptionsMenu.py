from menus.baseMenu import OptionValueBool, OptionValueInt, MenuOption
from game.env_variables import TAIL_BITING, TAIL_STEALING, set_config
from viewer.colors import Color
from controls.input_controls import Controls, menu_controls, general_controls
from menus.baseMenu import BaseMenu


class GameplayOptionsMenu(BaseMenu):
    def __init__(self, game):
        BaseMenu.__init__(self, game)
        self.name = "GameplayOptionsMenu"
        self.options = {
            "players": MenuOption(
                "players",
                optionValue=OptionValueInt(2, 1, 1, 4),
                function=self.set_players_function,
            ),
            "time limit": MenuOption(
                "time limit",
                optionValue=OptionValueInt(45, 5, 5, 90),
                function=self.set_time_limit_function,
            ),
            "countdown": MenuOption(
                "countdown",
                optionValue=OptionValueInt(3, 1, 0, 5),
                function=self.set_countdown_function,
            ),
            "tail biting": MenuOption(
                "tail biting",
                optionValue=OptionValueBool(TAIL_BITING),
                function=self.set_tail_biting_function,
            ),
            "tail stealing": MenuOption(
                "tail stealing",
                optionValue=OptionValueBool(TAIL_STEALING),
                function=self.set_tail_stealing_function,
            ),
            "snake speed": MenuOption(
                "snake speed",
                optionValue=OptionValueInt(4, 1, 1, 6),
                function=self.set_snake_speed_function,
            ),
        }
        self.selected_option = self.options["players"]

    def set_players_function(self):
        pass

    def set_time_limit_function(self):
        pass

    def set_countdown_function(self):
        pass

    def set_tail_biting_function(self):
        print(f"tail biting before set: {TAIL_BITING}")
        new_value = self.options["tail biting"].optionValue.value
        print(f"setting tail biting to {new_value}")
        set_config("mode", "TAIL_BITING", new_value)
        print(f"tail biting after set: {TAIL_BITING}")

    def set_tail_stealing_function(self):
        pass

    def set_snake_speed_function(self):
        pass
