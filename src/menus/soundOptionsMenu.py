from viewer.colors import Color
from controls.input_controls import Controls, menu_controls, general_controls
from menus.baseMenu import BaseMenu, MenuOption, OptionValueBool, OptionValueInt


class SoundOptionsMenu(BaseMenu):
    def __init__(self, game):
        BaseMenu.__init__(self, game)
        self.name = "SoundOptionsMenu"
        self.options = {
            "master volume": MenuOption(
                "master volume",
                optionValue=OptionValueInt(5, 1, 0, 10),
                function=self.set_master_volume_function,
            ),
            "music volume": MenuOption(
                "music volume",
                optionValue=OptionValueInt(5, 1, 0, 10),
                function=self.set_music_volume_function,
            ),
            "effects volume": MenuOption(
                "effects volume",
                optionValue=OptionValueInt(5, 1, 0, 10),
                function=self.set_effects_volume_function,
            ),
            "mute music": MenuOption(
                "mute music",
                optionValue=OptionValueBool(False),
                function=self.mute_music_function,
            ),
            "mute effects": MenuOption(
                "mute effects",
                optionValue=OptionValueBool(False),
                function=self.mute_effects_function,
            ),
        }
        self.selected_option = self.options["master volume"]

    def mute_music_function(self):
        if not self.game.sounds.music_paused:
            self.game.sounds.pause_music()
        else:
            self.game.sounds.unpause_music()

    def mute_effects_function(self):
        if not self.game.sounds.effects_muted:
            self.game.sounds.mute_effects()
        else:
            self.game.sounds.unmute_effects()

    def set_master_volume_function(self):
        pass

    def set_music_volume_function(self):
        pass

    def set_effects_volume_function(self):
        pass
