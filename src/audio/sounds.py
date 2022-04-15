import random
from game.env_variables import BITE_PLAYER_COLLISION_SOUND, BITE_SELF_COLLISION_SOUND, DEFEAT_SOUND, EFFECT_VOLUME, MUSIC_PATH, MUSIC_VOLUME, PLAYER_1_EAT_FRUIT_SOUNDS, PLAYER_2_EAT_FRUIT_SOUNDS, PLAYER_COLLISION_SOUND, SELF_COLLISION_SOUND, TEST_SOUND, VICTORY_SOUND, WALL_COLLISION_SOUND
import pygame

class Sounds:

    def __init__(self):
        self.mixer = pygame.mixer
        self.mixer.init()
        self.music = None #self.load_music()
        self.effects = {
            "test" : TEST_SOUND,
            #"eat_fruit" : ,
            # "player_collision" : PLAYER_COLLISION_SOUND,
            # "self_collision" : SELF_COLLISION_SOUND,
            # "bite_player_collision" : BITE_PLAYER_COLLISION_SOUND,
            # "bite_self_collision" : BITE_SELF_COLLISION_SOUND,
            # "wall_collision" : WALL_COLLISION_SOUND,
            # "victory" : VICTORY_SOUND,
            # "defeat" : DEFEAT_SOUND,
        }
        self.player_effects = {
            0 : PLAYER_1_EAT_FRUIT_SOUNDS,
            1 : PLAYER_2_EAT_FRUIT_SOUNDS,
            2 : PLAYER_1_EAT_FRUIT_SOUNDS,
            3 : PLAYER_2_EAT_FRUIT_SOUNDS,
            4 : PLAYER_1_EAT_FRUIT_SOUNDS,
            5 : PLAYER_2_EAT_FRUIT_SOUNDS,
            6 : PLAYER_1_EAT_FRUIT_SOUNDS,
            7 : PLAYER_2_EAT_FRUIT_SOUNDS,
        }

        self.music_volume = MUSIC_VOLUME
        self.effect_volume = EFFECT_VOLUME

        self.music_paused = False
        self.effects_muted = False

    def init(self):
        self.init_effects()
        self.init_player_effects()
        self.load_music(MUSIC_PATH)

    def load_music(self, path):
        self.mixer.music.load(path)

    def play_music(self):
        self.mixer.music.play(-1)

    def pause_music(self):
        self.mixer.music.pause()
        self.music_paused = True

    def unpause_music(self):
        self.mixer.music.unpause()
        self.music_paused = False

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

    def init_player_effects(self):
        for player in self.player_effects:
            effect_files = self.player_effects[player]
            self.player_effects[player] = []
            for effect in effect_files:
                self.player_effects[player].append(self.load_effect(effect))
        self.set_effect_volume(self.effect_volume)

    def load_effect(self, path):
        return pygame.mixer.Sound(path)

    def play_effect(self, effect):
        self.effects[effect].play()

    def play_player_effect(self, player):
        random.choice(self.player_effects[player]).play()

    def set_effect_volume(self, volume):
        for effect in self.effects:
            self.effects[effect].set_volume(volume)
        self.set_player_effect_volume(volume)

    def set_player_effect_volume(self, volume):
        for player in self.player_effects:
            for effect in self.player_effects[player]:
                effect.set_volume(volume)

    def mute_effects(self):
        self.set_effect_volume(0.0)
        self.effects_muted = True

    def unmute_effects(self):
        self.set_effect_volume(self.effect_volume)
        self.effects_muted = False


    def test(self):
        sound = self.load_effect("sounds\\release_snare.wav")
        sound.play()