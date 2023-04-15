from core.common_names import *

from core.event_holder import EventHolder
from core.assets import *
from core.camera import Camera

screen: Optional[pg.Surface] = None


event_holder: Optional[EventHolder] = None
game = None
camera = Camera(Vector2(0,0))
inner_box_list:list[Rect] = []
font: Optional[pg.Font] = None
little_font: Optional[pg.Font] = None
smallest_font: Optional[pg.Font] = None