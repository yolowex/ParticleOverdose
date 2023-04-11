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
        self.power = 1000

    @property
    def top_pos( self ):
        pos = self.pos.copy()
        x = 1000 - cr.event_holder.final_fps
        if x < 0:
            x = 0

        x+=50

        pos.y -= x
        return pos

    @property
    def move_unit( self ):
        return self.power * cr.event_holder.delta_time

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
        if self.power < 0 : return

        t = self.target_point
        diff = [t.x - self.pos.x,t.y - self.pos.y]
        unit = self.move_unit * 0.5
        x = abs(diff[0]) / unit
        diff = [diff[0] / x,diff[1] / x]

        self.power -= 1000 * cr.event_holder.delta_time

        self.pos.x += diff[0]
        self.pos.y += diff[1]



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