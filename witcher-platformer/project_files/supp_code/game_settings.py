import os

# Constants
SCREEN_WIDTH = 1152
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Witcher Platformer"
START = 0
END = 2000
STEP = 50

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
CHARACTER_SCALING = 1
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
COIN_SCALING = 0.25

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 200
RIGHT_VIEWPORT_MARGIN = 200
BOTTOM_VIEWPORT_MARGIN = 150
TOP_VIEWPORT_MARGIN = 100

'''
Settings containg game constants.
'''
# Scaling constants
MAP_SCALING = 1.25

# Player constants
PLAYER_START_X = 809.0
PLAYER_START_Y = 4849.0

PLAYER_END_X = 640.0
PLAYER_END_Y = [4908, 4985]

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

# Show Stats
STATS = False
# Fullscreen Mode
FULLSCREEN = False
# Level 1 Loaded
LOAD_LEVEL_1 = False

# Where your assets are directory is located
ASSET_PATH = os.path.join((os.path.dirname(os.path.dirname(__file__))), 'game_assets')
# Font path
FONT = os.path.join(ASSET_PATH, 'MinimalPixel2')