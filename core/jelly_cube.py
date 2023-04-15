from core.common_names import *
import core.common_resources as cr
from core.common_functions import *

class JellyCube:
    def __init__(self,points:list[Vector2]):
        self.original_points = points

        self.min_height = self.o_rect.height * 0.5
        self.original_height = self.o_rect.height
        self.max_height = self.o_rect.height * 2
        self.angle_change_power = 0
        self.jelly_swing_scale = 1

        self.min_angle = -45
        self.max_angle = 45
        self.points = [i.copy() for i in points]
        self.top_points_angle = 0
        self.is_moving = False
        self.is_charging = False
        self.is_jumping = False
        self.is_falling = False
        self.is_shaking = False
        self.is_still = False

    @property
    def height_scale( self ):
        a = percent(self.max_height-self.min_height,self.o_rect.height-self.min_height)
        a*=0.01
        if a<0:
            a = 0
        if a>1:
            a = 1
        return a

    @property
    def angle_speed(self):
        return 60 * cr.event_holder.delta_time

    def check_events( self ):
        self.is_shaking = False

        self.check_angle_change()
        self.check_size_change()

        self.is_still = not self.is_moving and not self.is_shaking \
                        and not self.is_jumping and not self.is_falling

    def rotate_points( self):
        for point,o_point in zip(self.points[:2],self.original_points[:2]):
            new_point = rotate_point(self.o_rect.center,o_point,self.top_points_angle)
            point.x,point.y = new_point


    def check_size_change( self ):
        lys = []

        if self.is_charging:
            m = 1
        elif self.is_jumping :
            m = -4
        elif self.is_falling :
            m = -2
        else:
            if self.o_rect.height > self.original_height:
                m = 4
            else:
                return


        for point in self.original_points[:2] :
            lys.append(point.copy())

            point.y += 100 * cr.event_holder.delta_time * m
            self.rotate_points()

        any_collision = False
        for rect in cr.game.inner_box_list:
            if self.rect.colliderect(rect):
                any_collision = True
                break
        # for
        # revert
        if not self.min_height <= self.o_rect.height <= self.max_height \
                or any_collision:
            for point, ly in zip(self.original_points[:2], lys) :
                point.x, point.y = ly.x, ly.y

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
            self.is_shaking = True and not self.is_moving

            if self.top_points_angle < self.min_angle:
                self.top_points_angle = self.min_angle
            if self.top_points_angle > self.max_angle:
                self.top_points_angle = self.max_angle

            self.rotate_points()



    def move( self,value:Vector2 ):
        hs = self.height_scale
        if hs < 0.5:
            hs = 0.5

        self.is_moving = True
        if value.x > 0:
            self.angle_change_power = - self.angle_speed * 10 * hs
            self.jelly_swing_scale = hs
        if value.x < 0:
            self.angle_change_power = self.angle_speed * 10 * hs
            self.jelly_swing_scale = hs

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

