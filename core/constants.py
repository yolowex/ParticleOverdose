from core.common_names import *
from core.common_resources import *

IS_WEB = __import__("sys").platform == "emscripten"

WHITE = Color(195,195,195)
BLACK = Color(15,15,15)
GRAY = WHITE.lerp(BLACK,0.5)
SKY = Color(150,150,220)
RED = Color(195,15,15)

RIGHT = 'right'
LEFT = 'left'

THROW = 'throw'
SWING = 'swing'
SWIRLING_THROW = 'swirling_throw'

THROW_TYPES = [THROW,SWIRLING_THROW]

ATTACK_NORMAL = 'normal'
ATTACK_SPECIAL = 'special'