import os
import configparser

config = configparser.RawConfigParser()
configFilePath = os.path.join("config", "config.cfg")
config.read(configFilePath)
# TODO Reload config after write

# Environment / Visual
Resolutions = {
    "x": [600, 1200, 1800, 2400, 3000],
    "y": [400, 800, 1200, 1600, 2000],
    "s": [
        10,
        20,
        30,
        40,
        50,
    ],
}
RESOLUTION_SCALE = config.getint("game", "RESOLUTION_SCALE")
SCREEN_SIZE_X = config.getint("game", "SCREEN_SIZE_X") * RESOLUTION_SCALE  # 1200
SCREEN_SIZE_Y = config.getint("game", "SCREEN_SIZE_Y") * RESOLUTION_SCALE  # 800
SNAKE_SIZE = config.getint("game", "SNAKE_SIZE") * RESOLUTION_SCALE  # 20
TICKS_PER_SECOND = config.getint("game", "TICKS_PER_SECOND")
FULLSCREEN = config.getboolean("game", "FULLSCREEN")

# Player
NUMBER_OF_PLAYERS = config.getint("player", "NUMBER_OF_PLAYERS")
INITIAL_FOOD = config.getint("player", "INITIAL_FOOD")
INITIAL_SNAKE_LENGTH = config.getint("player", "INITIAL_SNAKE_LENGTH")
INITIAL_LIVES = config.getint("player", "INITIAL_LIVES")
SNAKE_SPEED = config.getint("player", "SNAKE_SPEED")
DEATH_PUNISHMENT = config.getint("player", "DEATH_PUNISHMENT")

# Mode / Mechanics
TAIL_BITING = config.getboolean("mode", "TAIL_BITING")
TAIL_STEALING = config.getboolean("mode", "TAIL_STEALING")

# Gameplay
VERZET = config.getboolean("gameplay", "VERZET")
FREEZE_FRAMES_ON_BITTEN = config.getint(
    "gameplay", "FREEZE_FRAMES_ON_BITTEN"
)  # Only active if VERZET is True
START_COUNTDOWN = config.getint("gameplay", "START_COUNTDOWN")  # seconds
GAME_TIMER_SWITCH = config.getboolean("gameplay", "GAME_TIMER_SWITCH")
GAME_TIMER = config.getint("gameplay", "GAME_TIMER")  # seconds

# Cosmetic
BACKGROUND_VISUALS = config.getboolean("cosmetic", "BACKGROUND_VISUALS")
WAVE_RATE = config.getfloat("cosmetic", "WAVE_RATE")
MAX_COLOR_SCALE = config.getint(
    "cosmetic", "MAX_COLOR_SCALE"
)  # higher value (potentially) compresses the colourmap so the hue shift is shorter
NEIGHBOURHOOD_SHAPE = config.getint(
    "cosmetic", "NEIGHBOURHOOD_SHAPE"
)  # 0 for Von Neumann, 1 for Moore
AGENT_EFFECT_STEP_SIZE = config.getint("cosmetic", "AGENT_EFFECT_STEP_SIZE")
FREEZE_FRAMES_ON_EAT = config.getint("cosmetic", "FREEZE_FRAMES_ON_EAT")
PLAYER_SCORE_BOXES = config.getboolean("cosmetic", "PLAYER_SCORE_BOXES")
BODY_DECAY_RATE = config.getint("cosmetic", "BODY_DECAY_RATE")

# Controllers
ENABLE_CONTOLLERS = config.getboolean("controller", "ENABLE_CONTOLLERS")
CONTROLLER_DEADZONE = config.getfloat("controller", "CONTROLLER_DEADZONE")

# Music
MUSIC_PATH = os.path.join(
    "assets", "audio", "music", "track_1_loop.wav"
)  # os.path.join('assets', 'audio', 'soundFX', "track_1_loop.wav"
DISABLE_MUSIC = config.getboolean("music", "DISABLE_MUSIC")
MUSIC_VOLUME = config.getfloat(
    "music", "MUSIC_VOLUME"
)  # float in the range [0,1] where 0 is off, 1 is loudest

# Sounds
DISABLE_EFFECT_SOUNDS = config.getboolean("sound", "DISABLE_EFFECT_SOUNDS")
EFFECT_VOLUME = config.getfloat("sound", "EFFECT_VOLUME")

TEST_SOUND = os.path.join("assets", "audio", "soundFX", "release_snare.wav")
PLAYER_1_EAT_FRUIT_SOUNDS = [
    os.path.join("assets", "audio", "soundFX", "1_pickupsound_1_C.wav"),
    os.path.join("assets", "audio", "soundFX", "1_pickupsound_2_D.wav"),
    os.path.join("assets", "audio", "soundFX", "1_pickupsound_3_E.wav"),
    os.path.join("assets", "audio", "soundFX", "1_pickupsound_4_G.wav"),
    os.path.join("assets", "audio", "soundFX", "1_pickupsound_5_A.wav"),
    os.path.join("assets", "audio", "soundFX", "1_pickupsound_6_C.wav"),
]
PLAYER_2_EAT_FRUIT_SOUNDS = [
    os.path.join("assets", "audio", "soundFX", "2_pickupsound_1_C.wav"),
    os.path.join("assets", "audio", "soundFX", "2_pickupsound_2_D.wav"),
    os.path.join("assets", "audio", "soundFX", "2_pickupsound_3_E.wav"),
    os.path.join("assets", "audio", "soundFX", "2_pickupsound_4_G.wav"),
    os.path.join("assets", "audio", "soundFX", "2_pickupsound_5_A.wav"),
    os.path.join("assets", "audio", "soundFX", "2_pickupsound_6_C.wav"),
]
PLAYER_COLLISION_SOUND = ""
SELF_COLLISION_SOUND = ""
BITE_PLAYER_COLLISION_SOUND = ""
BITE_SELF_COLLISION_SOUND = ""
WALL_COLLISION_SOUND = ""
VICTORY_SOUND = ""  # "GAME!"
DEFEAT_SOUND = ""  # "PLAYER 1, DEFEATED"
# More for later: eat larger / golden fruit, powerups
