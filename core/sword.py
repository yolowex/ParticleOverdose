from core.common_names import *
import core.common_resources as cr
from core.sprite import Sprite
from core.constants import *
from core.common_functions import *
from core.particle import Particle


class Sword :

    def __init__( self ) :
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
        self.attack_key = None
        self.is_retrieving = False
        self.is_active = False
        self.last_attack_type = None
        self.was_thrown = False
        self.timer = None
        self.move_timer = None
        self.idle_duration = 1.5
        self.original_distance = 0.7
        self.distance = self.original_distance


    def init( self ) :
        name = 'blood'
        self.update_sword(name)
        self.rotate_sword()


    # @property
    # def is_active( self ):
    #     return self.distance > 0.25

    def reset_sword( self ):
        self.is_attacking = False
        self.is_retrieving = False
        self.angle = 0
        self.distance = 0.7
        self.move_timer = None
        self.timer = None
        self.rotate_sword()

    def rotate_sword( self ) :
        swords = [i.transformed_surface for i in [self.sword_right, self.sword_left]]

        r = 1
        for sword, drc in zip(swords, 'rl') :
            if drc == 'l' :
                r = -1

            new_sword = pg.transform.rotate(sword, -self.angle * r)
            # This code doesn't work for the opposite direction of the player because of this
            gp = self.get_grab_point(drc)

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

            if drc == 'r' :
                self.rotated_sword_right = new_sword
                self.rotated_points_right = r_points
            else :
                self.rotated_sword_left = new_sword
                self.rotated_points_left = r_points


    @property
    def grab_point( self ) :
        return self.get_grab_point(cr.game.player.facing)


    def get_grab_point( self, direction: str ) :
        if direction == 'r' :
            direction = RIGHT
        elif direction == 'l' :
            direction = LEFT

        player = cr.game.player
        ptl, pbl = player.points[0], player.points[3]
        ptr, pbr = player.points[1], player.points[2]

        b = pbr.lerp(pbl, 0.5)
        t = ptr.lerp(ptl, 0.5)
        c = b.lerp(t, 0.3)

        m = 1
        if self.name == 'blood' :
            m = 1.5
        if direction == RIGHT :
            c.x += player.rect.w * self.distance * m
        else :
            c.x -= player.rect.w * self.distance * m

        return c


    def update_sword( self, name: str ) :
        if self.name != name :
            self.name = name
            self.sword_left = cr.left_sword_dict[self.name]
            self.sword_right = cr.right_sword_dict[self.name]
            self.distance = self.original_distance
            self.is_attacking = False
            self.was_thrown = False
            self.is_retrieving = False
            self.angle = 0
            self.rotate_sword()
            self.timer = now()
            self.is_active = True



    def check_events( self ) :
        self.check_attack()
        self.angle += self.angle_power

        if K_f in cr.event_holder.pressed_keys :
            self.attack(ATTACK_NORMAL)
        if K_v in cr.event_holder.pressed_keys:
            if not self.is_attacking and not self.is_retrieving:
                self.attack(ATTACK_SPECIAL)
            elif not self.was_thrown and not self.is_attacking and not self.is_retrieving:
                self.reset_sword()
                self.timer = now()

        self.check_activeness()


    @property
    def angle_speed( self ) :
        return 2000 * cr.event_holder.delta_time


    def swing_attack( self, swing_speed: float = 1, release_speed: float = 0.5,
            swing_amount: float = 135 ) :

        angle_m = 1
        points = self.rotated_points_right
        if cr.game.player.facing == LEFT:
            points = self.rotated_points_left
            angle_m = -1

        for _ in range(random.randint(1,5)):
            b = points[2].lerp(points[3],0.5)
            t = points[0].lerp(points[1],0.5)

            shoot_point = b.lerp(t,0.5)
            shoot_angle = self.angle * angle_m
            size = random.uniform(1,4)
            self.add_particle(shoot_point,shoot_angle,size,BLACK)

        self.last_attack_type = SWING
        m = swing_speed
        if self.is_retrieving :
            m = -release_speed

        self.angle += self.angle_speed * m

        if self.angle >= swing_amount :
            self.angle = swing_amount
            self.angle = self.angle % 360
            self.is_retrieving = True
            self.is_attacking = False

        elif self.is_retrieving and self.angle <= 0 :
            self.angle = 0
            self.is_retrieving = False
            self.timer = now()

        self.rotate_sword()

    def throw_attack( self ):
        self.last_attack_type = THROW
        throw_angle = 90
        m = 0.5
        throw_speed = 20
        max_distance = 20

        # retrieve
        if self.was_thrown and self.distance != self.original_distance:
            self.is_attacking = False
            self.is_retrieving = True
            self.distance -= cr.event_holder.delta_time * throw_speed
            if self.distance < self.original_distance:
                self.distance = self.original_distance

        # rotate out
        elif self.was_thrown and self.distance == self.original_distance:
            self.angle -= self.angle_speed * m
            if self.angle < 0:
                self.angle = 0
                self.is_retrieving = False
                self.is_attacking = False
                self.was_thrown = False
                self.timer = now()
        else:
            # rotate in
            if self.angle < throw_angle :
                self.is_attacking = True
                self.angle += self.angle_speed * m
                if self.angle > throw_angle :
                    self.angle = throw_angle
            # throw
            elif self.angle == throw_angle :
                self.distance += cr.event_holder.delta_time * throw_speed
                if self.distance > max_distance :
                    self.distance = max_distance
                    self.was_thrown = True

        self.rotate_sword()


    def swirling_throw_attack( self ):
        self.last_attack_type = SWIRLING_THROW
        throw_angle = 90
        rotate_in_out = 0.5
        throw_m = 0.5
        retrieve_m = 0.5
        throw_speed = 15
        retrieve_speed = 15
        max_distance = 8

        # It's messy but I'm in a hurry
        def current_distance_scale():
            x = 1 - (self.distance / max_distance)
            x *= 2
            if x >= 1:
                x = 1
            if x <= 0.2:
                x = 0.2
            return x

        # retrieve
        if self.was_thrown and self.distance != self.original_distance:
            self.angle += self.angle_speed * retrieve_m
            self.is_attacking = False
            self.is_retrieving = True
            self.distance -= cr.event_holder.delta_time * retrieve_speed * current_distance_scale()
            if self.distance < self.original_distance:
                self.distance = self.original_distance
                self.angle = abs(self.angle)
                self.angle = self.angle % 360

        # rotate out
        elif self.was_thrown and self.distance == self.original_distance:

            dirc = -1
            if self.angle > 360-self.angle:
                dirc = 1

            self.angle += self.angle_speed * rotate_in_out * dirc
            if self.angle < 0 or self.angle > 360:
                self.angle = 0
                self.is_retrieving = False
                self.is_attacking = False
                self.was_thrown = False
                self.timer = now()
        else:
            # rotate in
            if self.angle < throw_angle:
                self.is_attacking = True
                self.angle += self.angle_speed * rotate_in_out
                if self.angle >= throw_angle :
                    self.angle = throw_angle
            # throw
            elif self.angle >= throw_angle:

                self.angle += self.angle_speed * throw_m
                self.distance += cr.event_holder.delta_time * throw_speed * current_distance_scale()
                if self.distance > max_distance :
                    self.distance = max_distance
                    self.was_thrown = True

        self.rotate_sword()

    def advance_attack( self,duration:float=0.5 ):


        dirc = cr.game.player.move_speed * 2.8
        if cr.game.player.facing == LEFT:
            dirc *= -1

        self.angle = 90
        self.rotate_sword()
        halt = False
        if not cr.game.player.move(Vector2(dirc,0),True):
            halt = True

        if self.move_timer is None:
            self.move_timer = now()

        elif self.move_timer + duration < now() or halt:
            self.angle = 0
            self.rotate_sword()
            self.move_timer = None
            self.is_attacking = False
            self.timer = now()
            return


    def fly_attack( self,duration:float=0.5 ):


        dirc = cr.game.player.move_speed * 3
        if cr.game.player.facing == LEFT:
            dirc *= -1

        self.angle = 0
        self.rotate_sword()
        halt = False
        if not cr.game.player.move(Vector2(0,-(abs(dirc))),True):
            halt = True

        if self.move_timer is None:
            self.move_timer = now()

        elif self.move_timer + duration < now() or halt:
            self.angle = 0
            self.rotate_sword()
            self.move_timer = None
            self.is_attacking = False
            self.timer = now()
            return

    def check_attack( self ) :
        if not self.is_attacking and not self.is_retrieving :
            return


        if self.attack_key == ATTACK_NORMAL:
            self.swing_attack()
        else:
            if self.name == 'death':
                self.throw_attack()

            if self.name == 'blood':
                self.swing_attack(1,0.1,360*3.1)

            if self.name == 'desire':
                self.swirling_throw_attack()

            if self.name == 'evil':
                self.swing_attack(2,4,360*10.8)

            if self.name == 'light':
                self.advance_attack(0.5)

            if self.name == 'hawk':
                self.fly_attack(0.5)


    def add_particle( self, source: Vector2, angle, size,color:Optional[Color]=None ) :
        if len(cr.game.particles) > cr.game.maximum_particles :
            return

        age = random.uniform(0, 1)
        cr.game.particles.append(Particle(source, size, angle, age,color,True,True))


    def check_activeness( self ) :
        if self.is_attacking or self.is_retrieving :
            return

        if self.timer is not None :
            if now() > self.timer + self.idle_duration :
                self.timer = None
                self.is_active = False


    def attack( self,attack_key) :
        if self.is_attacking or self.is_retrieving:
            return

        self.attack_key = attack_key
        self.is_attacking = True
        self.is_active = True


    def render_debug( self, points ) :
        pg.draw.polygon(cr.screen, 'red', points, width=2)


    def render( self ) :
        if not self.is_active :
            return

        points = self.rotated_points_right
        sword = self.rotated_sword_right
        if cr.game.player.facing == LEFT :
            points = self.rotated_points_left
            sword = self.rotated_sword_left

        points = [i.copy() for i in points]
        move_points(points,cr.camera.x,cr.camera.y)
        the_rect = polygon_to_rect(points)

        cr.screen.blit(sword, the_rect)

        if cr.event_holder.should_render_debug :
            self.render_debug(points)
