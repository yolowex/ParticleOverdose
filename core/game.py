from core.common_names import *
from core.player import Player
import core.common_resources as cr
from core.common_functions import *
from core.constants import *

class Game:
    def __init__(self):
        self.bg = WHITE

        s = cr.screen.get_size()
        # experimental
        self.box = FRect(s[0]*0.1,s[1]*0.1,s[0]*0.8,s[1]*0.8)
        self.box_width = int(s[0]*0.01)
        if self.box_width<1:
            self.box_width = 1

        p_rect = self.inner_box
        p_rect.w = p_rect.h = p_rect.w * 0.07
        p_rect.center = self.box.center
        self.player = Player(rect_convert_polygon(p_rect))
        self.gravity = Vector2(0,8)


    @property
    def delta_time( self ):
        return 1 / cr.event_holder.final_fps

    # experimental
    @property
    def inner_box( self ) -> FRect:

        rect = self.box.copy()
        rect.x+=self.box_width
        rect.y+=self.box_width
        rect.w-=self.box_width*2
        rect.h-=self.box_width*2
        return rect

    def check_events( self ):
        self.player.gravity_request(self.gravity.copy())
        self.player.check_events()

    def render( self ):
        cr.screen.fill(self.bg)
        pg.draw.rect(cr.screen,BLACK,self.box,width=self.box_width)
        pg.draw.rect(cr.screen,BLACK.lerp(WHITE,0.9),self.inner_box)
        self.player.render()
