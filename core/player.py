from core.common_names import *
import core.common_resources as cr
from core.constants import *
from core.jelly_cube import JellyCube


class Player(JellyCube) :

    def __init__( self, points: list[Vector2] ) :
        self.points = points
        self.color = WHITE
        self.border_color = BLACK.lerp(WHITE, 0.5)
        self.border_size = 5
        if self.border_size < 1 :
            self.border_size = 1

        self.gravity = Vector2(0, 0)

        # super(Player, self).__init__(points)


    @property
    def rect( self ) :
        x_list = [i.x for i in self.points]
        y_list = [i.y for i in self.points]
        min_x = min(x_list)
        max_x = max(x_list)
        min_y = min(y_list)
        max_y = max(y_list)

        return FRect(min_x, min_y, max_x - min_x, max_y - min_y)


    @property
    def center( self ) :
        return Vector2(self.rect.center)


    @center.setter
    def center( self, new_center: Vector2 ) :
        last_center = Vector2(self.rect.center)
        diff = Vector2(new_center.x - last_center.x, new_center.y - last_center.y)

        for point in self.points :
            point.x += diff.x
            point.y += diff.y


    def gravity_tick( self ) :



        last_center = self.center
        center = last_center.copy()
        center.x += self.gravity.x
        center.y += self.gravity.y
        self.gravity.x,self.gravity.y = (0,0)
        self.center = center
        if not cr.game.inner_box.contains(self.rect):
            self.center = last_center


    def gravity_request( self, gravity: Vector2 ) :
        self.gravity = gravity


    def check_events( self ) :
        self.gravity_tick()


    def render_debug( self ) :
        pg.draw.rect(cr.screen, "purple", self.rect)


    def render( self ) :
        if cr.event_holder.should_render_debug :
            self.render_debug()

        pg.draw.polygon(cr.screen, self.color, self.points)
        pg.draw.polygon(cr.screen, self.border_color, self.points, width=self.border_size)
