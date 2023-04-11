from core.common_names import *
from core.common_functions import *
import core.common_resources as cr

class Particle:
    def __init__(self,pos:Vector2,size:float,angle:int=0):
        self.pos = pos
        self.size = size
        self.color = random_color()
        self.angle = angle
        self.gravity = 0
        self.lerp_power = 0.07

    @property
    def top_pos( self ):
        pos = self.pos.copy()
        pos.y -= cr.screen.get_height() * 0.1
        return pos

    @property
    def target_point( self ):
        return rotate_point(self.pos,self.top_pos,self.angle)


    @property
    def rect( self ):
        rect = FRect(0,0,self.size,self.size)
        rect.center = self.pos
        return rect


    def check_events( self ):
        self.gravity_tick()
        self.move()

    def move( self ):
        if not self.lerp_power:
            return

        self.pos = self.pos.lerp(self.target_point,self.lerp_power)
        # self.lerp_power -= 0.001
        if self.lerp_power < 0 or self.lerp_power > 1:
            self.lerp_power = 0

    def render( self ):
        pg.draw.rect(cr.screen,self.color,self.rect)


    def gravity_tick( self ) :
        last_center = self.pos
        center = last_center.copy()

        center.y += self.gravity
        self.gravity = 0
        self.pos = center
        if not cr.game.inner_box.contains(self.rect):
            self.pos = last_center

    def gravity_request( self, gravity: float ) :
        self.gravity = gravity