from core.common_names import *
import core.common_resources as cr
from core.common_functions import *

class JellyCube:
    def __init__(self,points:list[Vector2]):
        self.original_points = points

        self.min_height = self.o_rect.height / 2
        self.original_height = self.o_rect.height
        self.max_height = self.o_rect.height * 2
        self.angle_change_power = 0
        self.jelly_swing_scale = 1

        self.min_angle = -45
        self.max_angle = 45
        self.points = [i.copy() for i in points]
        self.top_points_angle = 0
        self.is_moving = False

    @property
    def angle_speed(self):
        return 60 * cr.event_holder.delta_time

    def check_events( self ):
        h_keys = cr.event_holder.held_keys

        self.check_angle_change()

        if K_w in h_keys:
            lys = []
            for point in self.original_points[:2]:
                lys.append(point.y)
                point.y -= 1000 * cr.event_holder.delta_time
                self.rotate_points()

            if self.o_rect.height > self.max_height:
                for point,ly in zip(self.original_points[:2],lys) :
                    point.y = ly
                    self.rotate_points()

        if K_s in h_keys:
            lys = []
            for point in self.original_points[:2]:
                lys.append(point.y)
                point.y += 1000 * cr.event_holder.delta_time
                self.rotate_points()

            if self.o_rect.height < self.min_height:
                for point,ly in zip(self.original_points[:2],lys) :
                    point.y = ly
                    self.rotate_points()


        # if not self.is_moving:
        #     self.top_points_angle -= (abs(self.top_points_angle) / self.top_points_angle
        #                                 if self.top_points_angle!=0 else 1) \
        #                                     * self.angle_speed * 2
        #     self.rotate_points()

        self.is_moving = False

    def rotate_points( self ):

        for point,o_point in zip(self.points[:2],self.original_points[:2]):
            new_point = rotate_point(self.o_rect.center,o_point,self.top_points_angle)
            point.x,point.y = new_point

    def check_angle_change( self ):

        if not self.is_moving:
            a = self.top_points_angle
            p = self.angle_change_power
            self.jelly_swing_scale -= cr.event_holder.delta_time * 0.7

            if a <= self.min_angle * self.jelly_swing_scale and p < 0:
                self.angle_change_power = abs(self.angle_change_power)

            if a >= self.max_angle * self.jelly_swing_scale and p > 0:
                self.angle_change_power = - abs(self.angle_change_power)

            if self.jelly_swing_scale < 0.01:
                self.angle_change_power = 0
                self.top_points_angle = 0
                self.rotate_points()

        if self.angle_change_power != 0:
            self.top_points_angle += self.angle_change_power
            if self.top_points_angle < self.min_angle:
                self.top_points_angle = self.min_angle
            if self.top_points_angle > self.max_angle:
                self.top_points_angle = self.max_angle

            self.rotate_points()



    def move( self,value:Vector2 ):
        self.is_moving = True
        if value.x > 0:
            self.angle_change_power = - self.angle_speed * 4
            self.jelly_swing_scale = 0.5
        if value.x < 0:
            self.angle_change_power = self.angle_speed * 4
            self.jelly_swing_scale = 0.5

        self.rotate_points()


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

        self.sync_o_points_by_point(2)

