from core.common_names import *
import core.common_resources as cr
from core.sprite import Sprite
from core.constants import *

class Sword:
    def __init__(self):
        self.sword_left: Optional[Sprite] = None
        self.sword_right: Optional[Sprite] = None
        self.angle = 0
        self.name = "none'"
        self.distance = 0
        self.rect:Optional[FRect] = None

    def init( self ):
        name = 'blood'
        self.update_sword(name)
        self.rect = self.get_rect()

    @property
    def is_active( self ):
        return self.distance > 0.25

    def update_rect( self ):
        self.rect = self.get_rect()

    def get_rect(self,distance:float=1):
        self.distance = distance
        w,h = self.sword_left.transformed_surface.get_size()

        ptl, pbl = cr.game.player.points[0], cr.game.player.points[3]
        ptr, pbr = cr.game.player.points[1], cr.game.player.points[2]


        x_offset = -self.sword_left.transformed_surface.get_width() * distance
        pt, pb = ptl, pbl
        if cr.game.player.facing == RIGHT :
            pt, pb = ptr, pbr
            x_offset = self.sword_left.transformed_surface.get_width()* -(1-distance)

        pt, pb = pt.copy(), pb.copy()

        p = pb.lerp(pt,0.3)
        p.x += x_offset
        p.y -= h

        rect = FRect(p.x,p.y,w,h)

        any_coll = any([rect.colliderect(i) == True for i in cr.game.inner_box_list])
        if any_coll and distance>=0:
            return self.get_rect(distance-0.2)
        else:
            return rect

    def update_sword( self ,name:str):
        if self.name != name:
            self.name = name
            self.sword_left = cr.left_sword_dict[self.name]
            self.sword_right = cr.right_sword_dict[self.name]

    def check_events( self ):
        ...

    def render( self ):
        if not self.is_active:
            return

        sword = self.sword_right.transformed_surface
        if cr.game.player.facing == RIGHT:
            sword = self.sword_left.transformed_surface

        rect = self.rect.copy()
        rect.x += cr.camera.x
        rect.y += cr.camera.y


        cr.screen.blit(sword,rect)

