from core.common_names import *
from core.common_functions import *
import core.common_resources as cr
from core.constants import *

"""
this needs to be optimized!!
some optimization is done.
it still needs to be faster
my guess is that I should use numpy
"""


class Particle :

    def __init__( self, pos: Vector2, size: float, angle: int = 0, age: float = 5,
            color: Optional[Color] = None, anti_gravity=False,anti_collision=False ) :

        self.pos = pos
        self.size = size
        self.color = color
        if self.color is None :
            self.color = random_color()
        self.anti_gravity = anti_gravity
        self.anti_collision = anti_collision
        self.angle = angle
        self.gravity = 0
        self.power = 5
        self.power_decrease_scale = 0
        self.age = age
        self.init_time = now()
        self.absolute_age = age * 2.5
        self.destroy_time = None


    @property
    def top_pos( self ) :
        pos = self.pos.copy()
        x = 1000 - cr.event_holder.final_fps
        if x < 0 :
            x = 0

        x += 50

        pos.y -= x
        return pos



    @property
    def target_point( self ) :
        return rotate_point(self.pos, self.top_pos, self.angle)


    @property
    def rect( self ) :
        rect = FRect(0, 0, self.size, self.size)
        rect.center = self.pos
        return rect


    def check_events( self ) :
        if self.destroy_time is not None :
            return

        self.gravity_tick()
        self.move()


    def move( self ) :
        if self.power <= 0 :
            return
        last_center = self.pos.copy()

        delta_lerp = cr.event_holder.delta_time*0.1*self.power
        self.power -= cr.event_holder.delta_time*self.power_decrease_scale
        if delta_lerp>1:
            delta_lerp = 1

        self.pos = self.pos.lerp(self.target_point,delta_lerp)
        if self.anti_collision:
            return
        any_ = False
        for box in cr.game.inner_box_list :
            if box.colliderect(self.rect) :
                any_ = True
                break

        if any_ :
            self.pos = last_center
            self.angle -= random.randint(-50,50)


    def render( self ) :
        color = self.color
        if self.destroy_time is not None :
            color = GRAY

        rect = Rect(self.rect.x + cr.camera.x, self.rect.y + cr.camera.y, self.rect.w, self.rect.h)

        pg.draw.rect(cr.screen, color, rect)


    def gravity_tick( self ) :
        if self.anti_gravity:
            return

        last_center = self.pos
        center = last_center.copy()

        center.y += self.gravity
        self.gravity = 0
        self.pos = center
        if self.anti_collision:
            return

        any_ = False
        for box in cr.game.inner_box_list :
            if box.colliderect(self.rect) :
                any_ = True


        if any_ :
            if self.power <= 0 :
                self.destroy_time = now()
            self.pos = last_center


    def gravity_request( self, gravity: float ) :
        self.gravity = gravity
