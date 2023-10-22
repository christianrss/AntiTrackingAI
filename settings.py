WINDOW_WIDTH        = 800
WINDOW_HEIGHT       = 600
FRAMERATE           = 120
WORM_TRACKING_RATE  = 1
MAX_PLAYER_SPEED    = 16

OPC_E               = 0 # move west
OPC_NE              = 1 # move northeast
OPC_N               = 2 # move north
OPC_NW              = 3 # move northwest
OPC_W               = 4 # move west
OPC_SW              = 5 # move southwest
OPC_S               = 6 # move south
OPC_SE              = 7 # move southeast

OPC_STOP             = 8  # stop for a moment
OPC_RAND             = 9  # select a random direction
OPC_TEST_DIST        = 10 # test distance
OPC_TRACKING_EVASIVE = 11 # track fish evasive
OPC_END              = -1 # end pattern

MIN_LONELYNESS      = 100

MAX_CLIP_X = WINDOW_WIDTH - 1;
MAX_CLIP_Y = WINDOW_HEIGHT - 1;