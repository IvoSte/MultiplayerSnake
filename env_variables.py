# Environment / Visual
SCREEN_SIZE_X = 1200
SCREEN_SIZE_Y = 800
TICKS_PER_SECOND = 60
SNAKE_SIZE = 20

# Player
NUMBER_OF_PLAYERS = 4
INITIAL_FOOD = 3
INITIAL_SNAKE_LENGTH = 200
INITIAL_LIVES = 3
SNAKE_SPEED = 4
DEATH_PUNISHMENT = 5

# Mode / Mechanics
TAIL_BITING = True
TAIL_STEALING = False

# Cosmetic
BACKGROUND_VISUALS = True
MAX_COLOR_SCALE = 1 # higher value (potentially) compresses the colourmap so the hue shift is shorter
NEIGHBOURHOOD_SHAPE = 0 # 0 for Von Neumann, 1 for Moore
AGENT_EFFECT_STEP_SIZE = 5
FREEZE_FRAMES_ON_EAT = 2
PLAYER_SCORE_BOXES = True
BODY_DECAY_RATE = 15

# Controllers
CONTROLLER_DEADZONE = 0.45

# Music
MUSIC_PATH = ""

# Sounds
EAT_FRUIT_SOUND = ""
PLAYER_COLLISION_SOUND = ""
SELF_COLLISION_SOUND = ""
BITE_PLAYER_COLLISION_SOUND = ""
BITE_SELF_COLLISION_SOUND = ""
WALL_COLLISION_SOUND = ""
VICTORY_SOUND = ""
DEFEAT_SOUND = ""
# More for later: eat larger / golden fruit, powerups
