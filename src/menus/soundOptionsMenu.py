from viewer.colors import Color
from controls.input_controls import Controls, menu_controls, general_controls
from menus.baseMenu import BaseMenu


class SoundOptionsMenu(BaseMenu):
    def __init__(self, game):
        BaseMenu.__init__(self, game)
        self.name = "SoundOptionsMenu"
        self.state = "mute music"
        self.states = [
            "mute music",
            "mute effects",
            "master volume",
            "music volume",
            "effects volume",
        ]
        self.menu_functions = {
            "mute music": self.mute_music_function,
            "mute effects": self.mute_effects_function,
            "master volume": self.set_master_volume_function,
            "music volume": self.set_music_volume_function,
            "effects volume": self.set_effects_volume_function,
        }

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
