from core.common_names import *
import core.common_resources as cr
from core.sprite import Sprite
from core.constants import *
from core.common_functions import *

class Sword:
    def __init__(self):
        self.sword_left: Optional[Sprite] = None
        self.sword_right: Optional[Sprite] = None
        self.angle = 0
        self.name = "none'"

    def init( self ):
        name = 'blood'
        self.update_sword(name)

    # @property
    # def is_active( self ):
    #     return self.distance > 0.25

    @property
    def grab_point( self ):
        player = cr.game.player
        ptl, pbl = player.points[0], player.points[3]
        ptr, pbr = player.points[1], player.points[2]

        b = pbr.lerp(pbl,0.5)
        t = ptr.lerp(ptl,0.5)
        c = b.lerp(t,0.3)

        if player.facing == RIGHT:
            c.x += player.rect.w * 0.7
        else:
            c.x -= player.rect.w * 0.7

        return c


    def update_sword( self ,name:str):
        if self.name != name:
            self.name = name
            self.sword_left = cr.left_sword_dict[self.name]
            self.sword_right = cr.right_sword_dict[self.name]


    def check_events( self ):
        self.angle += cr.event_holder.delta_time * 50
        if K_f in cr.event_holder.pressed_keys:
            ...

    def render( self ):
        # if not self.is_active:
        #     return

        sword = self.sword_right.transformed_surface
        if cr.game.player.facing == RIGHT:
            sword = self.sword_left.transformed_surface

        new_sword = pg.transform.rotate(sword,self.angle).convert()
        gp = self.grab_point
        gp.x += cr.camera.x
        gp.y += cr.camera.y

        r_points = get_rotated_points(FRect(new_sword.get_rect()),-self.angle)
        ptl, pbl = r_points[0], r_points[3]
        ptr, pbr = r_points[1], r_points[2]

        b = pbr.lerp(pbl, 0.5)
        t = ptr.lerp(ptl, 0.5)
        c = b.lerp(t, 0.3)




        diff = gp.x - c.x, gp.y - c.y

        for point in r_points:
            point.x += diff[0]
            point.y += diff[1]

        x_list = [i.x for i in r_points]
        y_list = [i.y for i in r_points]
        min_x = min(x_list)
        max_x = max(x_list)
        min_y = min(y_list)
        max_y = max(y_list)
        the_rect = FRect(min_x, min_y, max_x - min_x, max_y - min_y)


        cr.screen.blit(new_sword,the_rect)
        pg.draw.polygon(cr.screen,"white",r_points,width=5)
