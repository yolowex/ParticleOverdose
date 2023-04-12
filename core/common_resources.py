from core.common_names import *

from core.event_holder import EventHolder
from core.assets import *
from core.camera import Camera

screen: Optional[pg.Surface] = None
event_holder: Optional[EventHolder] = None
game = None
camera = Camera(Vector2(0,0))
