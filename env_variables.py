import os

# Environment / Visual
Resolutions = {
    'x' : [600, 1200, 1800, 2400, 3000],
    'y' : [400, 800, 1200, 1600, 2000],
    's' : [10, 20, 30, 40, 50,]
}
RESOLUTION_SCALE = 3
SCREEN_SIZE_X = 600 * RESOLUTION_SCALE #1200
SCREEN_SIZE_Y = 400 * RESOLUTION_SCALE #800
SNAKE_SIZE = 10 * RESOLUTION_SCALE #20
TICKS_PER_SECOND = 60
FULLSCREEN = False

# Player
NUMBER_OF_PLAYERS = 2
INITIAL_FOOD = 1
INITIAL_SNAKE_LENGTH = 1
INITIAL_LIVES = 2
SNAKE_SPEED = 4
DEATH_PUNISHMENT = 5

# Mode / Mechanics
TAIL_BITING = True
TAIL_STEALING = True

# Gameplay
VERZET = False
FREEZE_FRAMES_ON_BITTEN = 300 # Only active if VERZET is True
START_COUNTDOWN = 3 # seconds
GAME_TIMER_SWITCH = False
GAME_TIMER = 90     # seconds

# Cosmetic
BACKGROUND_VISUALS = True
WAVE_RATE = 0.2
MAX_COLOR_SCALE = 3 # higher value (potentially) compresses the colourmap so the hue shift is shorter
NEIGHBOURHOOD_SHAPE = 0 # 0 for Von Neumann, 1 for Moore
AGENT_EFFECT_STEP_SIZE = 5
FREEZE_FRAMES_ON_EAT = 2
PLAYER_SCORE_BOXES = True
BODY_DECAY_RATE = 15

# Controllers
ENABLE_CONTOLLERS = True
CONTROLLER_DEADZONE = 0.45

# Music
MUSIC_PATH = os.path.join('sounds', 'track_1_loop.wav') #os.path.join("sounds", "track_1_loop.wav"
DISABLE_MUSIC = False
MUSIC_VOLUME = 1.0    # float in the range [0,1] where 0 is off, 1 is loudest

# Sounds
DISABLE_EFFECT_SOUNDS = False
EFFECT_VOLUME = 0.5

TEST_SOUND = os.path.join("sounds", "release_snare.wav")
PLAYER_1_EAT_FRUIT_SOUNDS = [os.path.join("sounds", "1_pickupsound_1_C.wav"),  os.path.join("sounds", "1_pickupsound_2_D.wav"), os.path.join("sounds", "1_pickupsound_3_E.wav"), os.path.join("sounds", "1_pickupsound_4_G.wav"), os.path.join("sounds", "1_pickupsound_5_A.wav"), os.path.join("sounds", "1_pickupsound_6_C.wav")]
PLAYER_2_EAT_FRUIT_SOUNDS = [os.path.join("sounds", "2_pickupsound_1_C.wav"),  os.path.join("sounds", "2_pickupsound_2_D.wav"), os.path.join("sounds", "2_pickupsound_3_E.wav"), os.path.join("sounds", "2_pickupsound_4_G.wav"), os.path.join("sounds", "2_pickupsound_5_A.wav"), os.path.join("sounds", "2_pickupsound_6_C.wav")]
PLAYER_COLLISION_SOUND = ""
SELF_COLLISION_SOUND = ""
BITE_PLAYER_COLLISION_SOUND = ""
BITE_SELF_COLLISION_SOUND = ""
WALL_COLLISION_SOUND = ""
VICTORY_SOUND = "" # "GAME!"
DEFEAT_SOUND = "" # "PLAYER 1, DEFEATED"
# More for later: eat larger / golden fruit, powerups
