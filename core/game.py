from core.common_names import *
from core.player import Player
import core.common_resources as cr
from core.common_functions import *
from core.constants import *
from core.level import Level

class Game:
    def __init__(self):
        self.bg = WHITE

        s = cr.screen.get_size()
        # experimental
        self.box = FRect(s[0]*0.1,s[1]*0.1,s[0]*0.8,s[1]*0.8)
        self.box_width = int(s[0]*0.01)
        if self.box_width<1:
            self.box_width = 1

        self.level = Level()

        p_rect = self.inner_box
        p_rect.w , p_rect.h = self.level.player_size
        p_rect.center = self.box.center
        self.player = Player(rect_convert_polygon(p_rect))
        print(self.level.player_pos)

        self.player.center = Vector2(self.level.player_pos)
        self.gravity = 500



    def init( self ):
        self.player.init()

        r_mouth = list(cr.right_mouth_sprite_dict.values())
        l_mouth = list(cr.left_mouth_sprite_dict.values())
        mouth = r_mouth + l_mouth
        for sprite in mouth:
            sprite.transform_by_width(self.player.rect.w * 0.5)
            if sprite in l_mouth:
                sprite.flip(flip_x = True)

        r_eye = list(cr.right_eye_sprite_dict.values())
        l_eye = list(cr.left_eye_sprite_dict.values())
        eye = r_eye + l_eye
        for sprite in eye:
            sprite.transform_by_width(self.player.rect.w * 0.5)
            if sprite in l_eye:
                sprite.flip(flip_x=True)



    # experimental
    @property
    def inner_box( self ) -> FRect:

        rect = self.box.copy()
        rect.x+=self.box_width
        rect.y+=self.box_width
        rect.w-=self.box_width*2
        rect.h-=self.box_width*2
        return rect

    # experimental
    @property
    def inner_box_list( self ):
        res = []
        cp = cr.camera.pos
        scr_rect = FRect(cr.screen.get_rect())
        scr_rect.x -= cp.x
        scr_rect.y -= cp.y

        return [i for i in self.level.inner_box_list if scr_rect.colliderect(i)]


    def check_events( self ):
        gravity = self.gravity
        gravity *= cr.event_holder.delta_time
        self.player.gravity_request(gravity)
        self.player.check_events()

    def render( self ):
        cr.screen.fill(self.bg)
        # pg.draw.rect(cr.surface,BLACK,self.box,width=self.box_width)
        # pg.draw.rect(cr.surface,BLACK.lerp(WHITE,0.9),self.inner_box)
        self.level.render()
        self.player.render()
