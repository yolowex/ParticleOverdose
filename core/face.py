from core.common_names import *
from core.common_functions import *
import core.common_resources as cr
from core.sprite import Sprite
from core.constants import *

class Face:

    def __init__( self ):
        self.eye_right: Optional[Sprite] = None
        self.mouth_right: Optional[Sprite]  = None
        self.eye_left: Optional[Sprite]  = None
        self.mouth_left: Optional[Sprite]  = None

        self.eye = "none"
        self.mouth = "none"


    def init( self ):
        eye = "angry"
        mouth = "smirk_0"
        self.update_face(eye,mouth)


    def update_face( self,new_eye=None,new_mouth=None ):

        if new_eye is not None and new_eye!=self.eye:
            self.eye = new_eye
            self.eye_right = cr.right_eye_sprite_dict[new_eye]
            self.eye_left = cr.left_eye_sprite_dict[new_eye]

        if new_mouth is not None and new_mouth!=self.mouth:
            self.mouth = new_mouth
            self.mouth_right = cr.right_mouth_sprite_dict[new_mouth]
            self.mouth_left = cr.left_mouth_sprite_dict[new_mouth]


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

        rect.x += cr.camera.x
        rect.y += cr.camera.y

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

        rect.x += cr.camera.x
        rect.y += cr.camera.y

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
