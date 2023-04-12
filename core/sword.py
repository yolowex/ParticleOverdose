from core.common_names import *
import core.common_resources as cr
from core.sprite import Sprite
from core.constants import *
from core.common_functions import *

class Sword:
    def __init__(self):
        self.sword_left: Optional[Sprite] = None
        self.sword_right: Optional[Sprite] = None
        self.angle = 0
        self.name = "none'"

    def init( self ):
        name = 'blood'
        self.update_sword(name)

    # @property
    # def is_active( self ):
    #     return self.distance > 0.25

    @property
    def grab_point( self ):
        ptl, pbl = cr.game.player.points[0], cr.game.player.points[3]
        ptr, pbr = cr.game.player.points[1], cr.game.player.points[2]

        b = pbr.lerp(pbl,0.5)
        t = ptr.lerp(ptl,0.5)
        c = b.lerp(t,0.5)
        return c


    def update_sword( self ,name:str):
        if self.name != name:
            self.name = name
            self.sword_left = cr.left_sword_dict[self.name]
            self.sword_right = cr.right_sword_dict[self.name]


    def check_events( self ):
        self.angle += cr.event_holder.delta_time * 50
        if K_f in cr.event_holder.pressed_keys:
            ...

    def render( self ):
        # if not self.is_active:
        #     return

        sword = self.sword_right.transformed_surface
        if cr.game.player.facing == RIGHT:
            sword = self.sword_left.transformed_surface

        new_sword = pg.transform.rotate(sword,self.angle).convert()


        gp = self.grab_point
        gp.x += cr.camera.x
        gp.y += cr.camera.y

        print(gp,cr.game.player.rect)
        cr.screen.blit(new_sword,gp)

