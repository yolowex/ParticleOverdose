from core.common_names import *
import core.common_resources as cr


class JellyCube :

    def __init__( self, points: list[Vector2] ) :
        self.points = points
        self.original_points = [i.copy() for i in self.points]
        self.is_moving = False
        self.is_falling = False


    @property
    def point_rel_value( self ) :
        v = cr.event_holder.delta_time * 2
        if v > 1 : v = 1
        return v


    def sync_points( self ) :
        v1,v0 = self.point_rel_value,self.point_rel_value*0.5

        if not self.is_moving:
            v1 *= 2

        for a, b, c in zip(self.points, self.original_points, range(len(self.points))) :
            cv = v1
            if c <= 1 : cv = v0
            self.points[c] = a.lerp(b, cv)


    def check_events( self ) :
        self.is_moving = self.is_falling = False
        self.sync_points()


    @property
    def original_rect( self ) :
        x_list = [i.x for i in self.original_points]
        y_list = [i.y for i in self.original_points]
        min_x = min(x_list)
        max_x = max(x_list)
        min_y = min(y_list)
        max_y = max(y_list)

        return FRect(min_x, min_y, max_x - min_x, max_y - min_y)


    @property
    def center( self ) :
        return Vector2(self.original_rect.center)


    @center.setter
    def center( self, new_center: Vector2 ) :
        last_center = Vector2(self.original_rect.center)
        diff = Vector2(new_center.x - last_center.x, new_center.y - last_center.y)

        for point in self.original_points :
            point.x += diff.x
            point.y += diff.y


    @property
    def rect( self ) :
        x_list = [i.x for i in self.points]
        y_list = [i.y for i in self.points]
        min_x = min(x_list)
        max_x = max(x_list)
        min_y = min(y_list)
        max_y = max(y_list)

        return FRect(min_x, min_y, max_x - min_x, max_y - min_y)
