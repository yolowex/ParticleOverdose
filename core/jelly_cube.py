from core.common_names import *
import core.common_resources as cr
from core.common_functions import *

class JellyCube:
    def __init__(self,points:list[Vector2]):
        self.original_points = points
        self.points = [i.copy() for i in points]
        self.top_points_angle = 0

    def check_events( self ):
        h_keys = cr.event_holder.held_keys

        if K_q in h_keys:
            self.top_points_angle -= 60 * cr.event_holder.delta_time
            self.rotate_points()
        if K_e in h_keys:
            self.top_points_angle += 60 * cr.event_holder.delta_time
            self.rotate_points()

    def rotate_points( self ):

        for point,o_point in zip(self.points[:2],self.original_points[:2]):
            new_point = rotate_point(self.o_rect.center,o_point,self.top_points_angle)
            point.x,point.y = new_point

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
    def o_rect( self ) :
        x_list = [i.x for i in self.original_points]
        y_list = [i.y for i in self.original_points]
        min_x = min(x_list)
        max_x = max(x_list)
        min_y = min(y_list)
        max_y = max(y_list)

        return FRect(min_x, min_y, max_x - min_x, max_y - min_y)

    def sync_o_points_by_point( self,index ):
        point = self.points[index]
        target = self.original_points[index]
        px,py = point
        tx,ty = target
        dx,dy = tx-px,ty-py

        for point in self.original_points:
            point.x-=dx
            point.y-=dy

        print(self.o_rect)


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
        print(self.o_rect)

        self.sync_o_points_by_point(2)

