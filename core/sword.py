from core.common_names import *
import core.common_resources as cr
from core.sprite import Sprite
from core.constants import *
from core.common_functions import *

class Sword:
    def __init__(self):
        self.sword_left: Optional[Sprite] = None
        self.sword_right: Optional[Sprite] = None
        self.rotated_sword_left: Optional[Surface] = None
        self.rotated_sword_right: Optional[Surface] = None
        self.rotated_points_left: list[Vector2] = []
        self.rotated_points_right: list[Vector2] = []
        self.angle = 0.0
        self.name = "none'"
        self.angle_power = 0.0
        self.is_attacking = False
        self.is_releasing = False
        self.is_active = False
        self.attack_end_time = None

    def init( self ):
        name = 'blood'
        self.update_sword(name)
        self.rotate_sword()


    # @property
    # def is_active( self ):
    #     return self.distance > 0.25

    def rotate_sword( self ):
        swords = [i.transformed_surface for i in [self.sword_right,self.sword_left]]

        r = 1
        for sword,drc in zip(swords,'rl'):
            if drc == 'l':
                r = -1

            new_sword = pg.transform.rotate(sword, -self.angle * r)
            # This code doesn't work for the opposite direction of the player because of this
            gp = self.get_grab_point(drc)
            gp.x += cr.camera.x
            gp.y += cr.camera.y

            r_points = get_rotated_points(FRect(sword.get_rect()), self.angle * r)

            ptl, pbl = r_points[0], r_points[3]
            ptr, pbr = r_points[1], r_points[2]

            b = pbr.lerp(pbl, 0.5)
            t = ptr.lerp(ptl, 0.5)
            c = b.lerp(t, 0.2)

            diff = gp.x - c.x, gp.y - c.y

            for point in r_points :
                point.x += diff[0]
                point.y += diff[1]

            if drc=='r':
                self.rotated_sword_right = new_sword
                self.rotated_points_right = r_points
            else:
                self.rotated_sword_left = new_sword
                self.rotated_points_left = r_points



    @property
    def grab_point( self ):
        return self.get_grab_point(cr.game.player.facing)


    def get_grab_point( self,direction:str ):
        if direction == 'r':
            direction = RIGHT
        elif direction == 'l':
            direction = LEFT

        player = cr.game.player
        ptl, pbl = player.points[0], player.points[3]
        ptr, pbr = player.points[1], player.points[2]

        b = pbr.lerp(pbl, 0.5)
        t = ptr.lerp(ptl, 0.5)
        c = b.lerp(t, 0.3)

        m = 1
        if self.name == 'blood':
            m = 1.5
        if direction == RIGHT :
            c.x += player.rect.w * 0.7 * m
        else :
            c.x -= player.rect.w * 0.7 * m

        return c
    def update_sword( self ,name:str):
        if self.name != name:
            self.name = name
            self.sword_left = cr.left_sword_dict[self.name]
            self.sword_right = cr.right_sword_dict[self.name]
            self.rotate_sword()

    def check_events( self ):
        self.angle += self.angle_power
        if K_f in cr.event_holder.pressed_keys:
            self.attack()

        self.check_attack()

    @property
    def angle_speed( self ) :
        return 2000 * cr.event_holder.delta_time

    def check_attack( self ):
        if not self.is_attacking and not self.is_releasing:
            return

        m = 1
        if self.is_releasing:
            m = -0.25

        self.angle += self.angle_speed * m

        if self.angle >= 180:
            self.is_releasing = True

        if self.is_releasing and self.angle<=0:
            self.angle = 0
            self.is_attacking = self.is_releasing = False
            self.attack_end_time = now()

        self.rotate_sword()


    def attack( self ):
        self.is_attacking = True
        self.is_active = True

    def render_debug( self,points ):
        pg.draw.polygon(cr.screen,'red',points,width=2)

    def render( self ):
        points = self.rotated_points_right
        sword = self.rotated_sword_right
        if cr.game.player.facing == LEFT:
            points = self.rotated_points_left
            sword = self.rotated_sword_left

        the_rect = polygon_to_rect(points)

        cr.screen.blit(sword,the_rect)

        if cr.event_holder.should_render_debug:
            self.render_debug(points)
