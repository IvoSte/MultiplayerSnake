# Environment / Visual
SCREEN_SIZE_X = 1200
SCREEN_SIZE_Y = 800
TICKS_PER_SECOND = 60
SNAKE_SIZE = 20

# Player
NUMBER_OF_PLAYERS = 1
INITIAL_FOOD = 3
INITIAL_SNAKE_LENGTH = 10
INITIAL_LIVES = 2
SNAKE_SPEED = 4
DEATH_PUNISHMENT = 5

# Mode / Mechanics
TAIL_BITING = True
TAIL_STEALING = False

# Gameplay
VERZET = True
FREEZE_FRAMES_ON_BITTEN = 0#120 # Only active if VERZET is True

# Cosmetic
BACKGROUND_VISUALS = True
WAVE_RATE = 0.2
MAX_COLOR_SCALE = 1 # higher value (potentially) compresses the colourmap so the hue shift is shorter
NEIGHBOURHOOD_SHAPE = 0 # 0 for Von Neumann, 1 for Moore
AGENT_EFFECT_STEP_SIZE = 5
FREEZE_FRAMES_ON_EAT = 2
PLAYER_SCORE_BOXES = True
BODY_DECAY_RATE = 15

# Controllers
ENABLE_CONTOLLERS = True
CONTROLLER_DEADZONE = 0.45

# Music
MUSIC_PATH = "sounds\\track_1_loop.wav"
DISABLE_MUSIC = True
MUSIC_VOLUME = 1.0    # float in the range [0,1] where 0 is off, 1 is loudest

# Sounds
DISABLE_EFFECT_SOUNDS = False
EFFECT_VOLUME = 1.0

TEST_SOUND = "sounds\\release_snare.wav"
PLAYER_1_EAT_FRUIT_SOUNDS = ["sounds\\1_pickupsound_1_C.wav", "sounds\\1_pickupsound_2_D.wav","sounds\\1_pickupsound_3_E.wav","sounds\\1_pickupsound_4_G.wav","sounds\\1_pickupsound_5_A.wav","sounds\\1_pickupsound_6_C.wav"]
PLAYER_2_EAT_FRUIT_SOUNDS = ["sounds\\2_pickupsound_1_C.wav", "sounds\\2_pickupsound_2_D.wav","sounds\\2_pickupsound_3_E.wav","sounds\\2_pickupsound_4_G.wav","sounds\\2_pickupsound_5_A.wav","sounds\\2_pickupsound_6_C.wav"]
PLAYER_COLLISION_SOUND = "" 
SELF_COLLISION_SOUND = ""
BITE_PLAYER_COLLISION_SOUND = ""
BITE_SELF_COLLISION_SOUND = ""
WALL_COLLISION_SOUND = ""
VICTORY_SOUND = "" # "GAME!"
DEFEAT_SOUND = "" # "PLAYER 1, DEFEATED"
# More for later: eat larger / golden fruit, powerups
