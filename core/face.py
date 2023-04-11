from core.common_names import *
from core.common_functions import *
import core.common_resources as cr
from core.sprite import Sprite
from core.constants import *

class Face:

    def __init__( self ):
        self.eye_right = Sprite("./assets/face/angry_eye.png")
        self.mouth_right = Sprite("./assets/face/smirk_1.png")
        self.eye_left = Sprite("./assets/face/angry_eye.png")
        self.mouth_left = Sprite("./assets/face/smirk_0.png")


    def init( self ):
        self.eye_right.transform_by_width(cr.game.player.rect.w*.5)
        self.mouth_right.transform_by_width(cr.game.player.rect.w*.5)
        self.eye_left.transform_by_width(cr.game.player.rect.w * .5)
        self.eye_left.flip(True)
        self.mouth_left.transform_by_width(cr.game.player.rect.w * .5)
        self.mouth_left.flip(True)


    @property
    def eye_rect( self ):
        ptl,pbl = cr.game.player.points[0],cr.game.player.points[3]
        ptr,pbr = cr.game.player.points[1],cr.game.player.points[2]

        pt,pb = ptl,pbl
        if cr.game.player.facing == RIGHT:
            pt,pb = ptr,pbr

        pt,pb = pt.copy(),pb.copy()

        pm = pb.lerp(pt,0.9)

        rect = self.eye_left.transformed_surface.get_rect()

        if cr.game.player.facing == RIGHT :
            rect.x,rect.y = pm.x-rect.w,pm.y
        else:
            rect.x,rect.y = pm

        return rect


    @property
    def mouth_rect( self ) :
        ptl, pbl = cr.game.player.points[0], cr.game.player.points[3]
        ptr, pbr = cr.game.player.points[1], cr.game.player.points[2]

        pt, pb = ptl, pbl
        if cr.game.player.facing == RIGHT :
            pt, pb = ptr, pbr

        pt, pb = pt.copy(), pb.copy()

        pm = pb.lerp(pt, 0.3)

        rect = self.mouth_left.transformed_surface.get_rect()

        if cr.game.player.facing == RIGHT :
            rect.x, rect.y = pm.x - rect.w, pm.y
        else :
            rect.x, rect.y = pm

        return rect

    def check_events( self ):
        ...

    def render( self ):
        eye = self.eye_right
        mouth = self.mouth_right

        if cr.game.player.facing == LEFT:
            eye = self.eye_left
            mouth = self.mouth_left

        cr.screen.blit(eye.transformed_surface,self.eye_rect)
        cr.screen.blit(mouth.transformed_surface,self.mouth_rect)
