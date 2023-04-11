from core.common_names import *

from core.event_holder import EventHolder
from core.assets import right_mouth_sprite_dict, right_eye_sprite_dict, left_mouth_sprite_dict, \
    left_eye_sprite_dict

screen: Optional[pg.Surface] = None
event_holder: Optional[EventHolder] = None
game = None
