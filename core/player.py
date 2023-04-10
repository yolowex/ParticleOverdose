from core.common_names import *
import core.common_resources as cr
from core.constants import *
from core.jelly_cube import JellyCube


class Player(JellyCube) :

    def __init__( self, points: list[Vector2] ) :
        self.color = WHITE
        self.border_color = BLACK.lerp(WHITE, 0.5)
        self.border_size = 1
        if self.border_size < 1 :
            self.border_size = 1

        self.move_speed = 300
        self.gravity = 0
        self.jump_power = -2000
        self.remaining_jump_power = 0

        super(Player, self).__init__(points)


    # temp
    def is_in_box( self ) :
        return cr.game.inner_box.contains(self.rect) and cr.game.inner_box.contains(
            self.original_rect)


    def gravity_tick( self ) :
        last_center = self.center
        center = last_center.copy()

        center.y += self.gravity
        self.gravity = 0
        self.center = center
        if not self.is_in_box() :
            self.center = last_center
        else:
            self.is_falling = True


    def gravity_request( self, gravity: float ) :
        self.gravity = gravity


    def move( self, value: Vector2 ) :
        self.is_moving = True
        # print(self.original_points[0],self.points[0])
        last_center = self.center
        center = last_center.copy()
        center.x += value.x * cr.event_holder.delta_time
        center.y += value.y * cr.event_holder.delta_time
        self.center = center
        if not self.is_in_box() :
            self.center = last_center


    def jump_request( self ) :
        self.remaining_jump_power = self.jump_power


    def check_jump( self ) :
        last_center = self.center
        center = last_center.copy()
        center.y += self.remaining_jump_power * cr.event_holder.delta_time
        self.center = center

        if not self.is_in_box() :
            self.center = last_center
            self.remaining_jump_power = 0
        else :
            self.remaining_jump_power -= (
                        self.remaining_jump_power * 7 * cr.event_holder.delta_time)
            if abs(self.remaining_jump_power) < abs(cr.game.gravity * 0.5) :
                self.remaining_jump_power = 0


    def check_movements( self ) :
        h_keys = cr.event_holder.held_keys
        p_keys = cr.event_holder.pressed_keys
        if K_RIGHT in h_keys or K_d in h_keys :
            self.move(Vector2(self.move_speed, 0))

        if K_LEFT in h_keys or K_a in h_keys :
            self.move(Vector2(-self.move_speed, 0))

        if K_SPACE in p_keys :
            self.jump_request()


    def check_events( self ) :
        super(Player, self).check_events()
        self.check_movements()
        self.check_jump()
        self.gravity_tick()


    def render_debug( self ) :
        pg.draw.rect(cr.screen, Color("purple").lerp(WHITE,0.9), self.rect)


    def render( self ) :
        if cr.event_holder.should_render_debug :
            self.render_debug()

        pg.draw.polygon(cr.screen, self.color, self.points)
        pg.draw.polygon(cr.screen, self.color, self.original_points)

        pg.draw.polygon(cr.screen, self.border_color, self.points, width=self.border_size)
