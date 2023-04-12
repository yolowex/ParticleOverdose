from core.common_names import *
from core.common_functions import *
import core.common_resources as cr
from core.constants import *

"""
this needs to be optimized!!

"""
class Particle:
    def __init__(self,pos:Vector2,size:float,angle:int=0,age:float=5):
        self.pos = pos
        self.size = size
        self.color = random_color()
        self.angle = angle
        self.gravity = 0
        self.power = 1000
        self.age = age
        self.destroy_time = None

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
        if self.destroy_time is not None:
            return

        self.gravity_tick()
        self.move()

    def move( self ):
        if self.power <= 0 :
            return
        last_center = self.pos.copy()

        t = self.target_point
        diff = [t.x - self.pos.x,t.y - self.pos.y]
        unit = self.move_unit * 0.5
        # hit an error here
        if unit == 0:
            return
        x = abs(diff[0]) / unit
        if x == 0:
            x = 1
        y = abs(diff[0]) / unit
        if y == 0 :
            y = 1

        diff = [diff[0] / x,diff[1] / y]

        self.power -= 1000 * cr.event_holder.delta_time

        self.pos.x += diff[0]
        self.pos.y += diff[1]

        any_ = False
        for box in cr.game.inner_box_list :
            if box.colliderect(self.rect) :
                any_ = True
                break

        if any_ :
            self.pos = last_center
            self.angle -= 180

    def render( self ):
        color = self.color
        if self.destroy_time is not None:
            color = GRAY

        rect = Rect(self.rect.x+cr.camera.x,self.rect.y+cr.camera.y,self.rect.w,self.rect.h)

        pg.draw.rect(cr.screen,color,rect)


    def gravity_tick( self ) :
        last_center = self.pos
        center = last_center.copy()

        center.y += self.gravity
        self.gravity = 0
        self.pos = center
        any_ = False
        for box in cr.game.inner_box_list:
            if box.colliderect(self.rect):
                any_ = True

        if any_:
            if self.power <= 0 :
                self.destroy_time = now()
            self.pos = last_center

    def gravity_request( self, gravity: float ) :
        self.gravity = gravity