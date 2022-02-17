from env_variables import BITE_PLAYER_COLLISION_SOUND, BITE_SELF_COLLISION_SOUND, DEFEAT_SOUND, EAT_FRUIT_SOUND, PLAYER_COLLISION_SOUND, SELF_COLLISION_SOUND, VICTORY_SOUND, WALL_COLLISION_SOUND
import pygame

class Sounds:

    def __init__(self):
        self.mixer = pygame.mixer
        self.mixer.init()
        self.music = self.load_music()
        self.effects = {
            "eat_fruit" : EAT_FRUIT_SOUND,
            "player_collision" : PLAYER_COLLISION_SOUND,
            "self_collision" : SELF_COLLISION_SOUND,
            "bite_player_collision" : BITE_PLAYER_COLLISION_SOUND,
            "bite_self_collision" : BITE_SELF_COLLISION_SOUND,
            "wall_collision" : WALL_COLLISION_SOUND,
            "victory" : VICTORY_SOUND,
            "defeat" : DEFEAT_SOUND,
        }

    def load_music(self, path):
        self.mixer.music.load(path)

    def play_music(self):
        self.mixer.music.play(-1)

    def pause_music(self):
        self.mixer.music.pause()

    def unpause_music(self):
        self.mixer.music.unpause()

    def restart_music(self):
        self.mixer.music.rewind()

    def stop_music(self):
        self.mixer.music.stop()

    def decrease_music_volume(self):
        self.set_music_volume(0.3)

    def increase_music_volume(self):
        self.set_music_volume(1.0)

    def set_music_volume(self, volume):
        self.mixer.music.set_volume(volume)

    def init_effects(self):
        for effect in self.effects:
            self.effects[effect] = self.load_effect(self.effects[effect])

    def load_effect(self, path):
        return pygame.mixer.Sound(path)

    def play_effect(self, effect):
        self.mixer.Sound.play(self.effects[effect])
        self.mixer.Sound.stop()

    def play_effect_alt(self, effect):
        self.effects[effect].play()