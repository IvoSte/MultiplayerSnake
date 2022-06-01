from viewer.colors import Color
from .baseMenuView import BaseMenuView, OptionText, Cursor, OptionValueView


class GameplayOptionsMenuView(BaseMenuView):
    def __init__(self, viewer, menu):
        BaseMenuView.__init__(self, viewer, menu)
        self.options = {
            "players": OptionText("Players", Color.WHITE.value, 0.5, 0.4),
            "time limit": OptionText("Time Limit", Color.WHITE.value, 0.5, 0.5),
            "countdown": OptionText("Countdown", Color.WHITE.value, 0.5, 0.6),
            "tail biting": OptionText("Tail Biting", Color.WHITE.value, 0.5, 0.7),
            "tail stealing": OptionText("Tail Stealing", Color.WHITE.value, 0.5, 0.8),
            "snake speed": OptionText("Snake Speed", Color.WHITE.value, 0.5, 0.9),
        }
        self.option_values = {
            "players": OptionValueView(Color.WHITE.value),
            "time limit": OptionValueView(Color.WHITE.value),
            "tail biting": OptionValueView(Color.WHITE.value)
        }

        self.cursor = Cursor("*", Color.WHITE.value, 0.0, 0.0, -0.05, 0.01)
