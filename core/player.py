from core.common_names import *
import core.common_resources as cr
from core.constants import *
from core.jelly_cube import JellyCube
from core.particle import Particle
from core.face import Face

class Player(JellyCube) :

    def __init__( self, points: list[Vector2] ) :
        self.color = WHITE
        self.border_color = BLACK.lerp(WHITE, 0.5)
        self.border_size = 1
        if self.border_size < 1 :
            self.border_size = 1

        self.face = Face()
        self.move_speed = 300
        self.gravity = 0
        self.jump_power = 0

        self.max_jump_power = -5000
        self.min_jump_power = -1500
        self.remaining_jump_power = 0

        self.maximum_particles = 1000
        self.particles = []
        self.facing = RIGHT

        super(Player, self).__init__(points)


    def init( self ):
        self.face.init()

    @property
    def jump_power_per_second( self ):
        return self.min_jump_power * cr.event_holder.delta_time


    def gravity_tick( self ) :
        last_center = self.center
        center = last_center.copy()

        center.y += self.gravity
        self.gravity = 0
        self.center = center
        if not cr.game.inner_box.contains(self.rect):
            self.center = last_center
            self.is_falling = False

    def gravity_request( self, gravity: float ) :
        self.gravity = gravity
        for particle in self.particles:
            particle.gravity_request(gravity)


    def move( self,value:Vector2 ):
        if value.x < 0:
            self.facing = LEFT
        elif value.x > 0:
            self.facing = RIGHT

        self.manage_movement_particles(value)
        last_center = self.center
        center = last_center.copy()
        center.x += value.x * cr.event_holder.delta_time
        center.y += value.y * cr.event_holder.delta_time
        self.center = center
        if not cr.game.inner_box.contains(self.rect) :
            self.center = last_center
        else:
            self.is_moving = True
            super(Player, self).move(value)

    def jump_request( self ):
        self.is_jumping = True
        self.face.update_face(new_mouth="talk_1")
        self.remaining_jump_power = self.jump_power

    def check_jump( self ):
        last_center = self.center
        center = last_center.copy()
        center.y += self.remaining_jump_power * cr.event_holder.delta_time
        self.center = center

        if not cr.game.inner_box.contains(self.rect) :
            self.center = last_center
            self.remaining_jump_power = 0
            self.is_jumping = False
            self.is_falling = True

        else:
            self.remaining_jump_power -= (self.remaining_jump_power*7*cr.event_holder.delta_time)
            if abs(self.remaining_jump_power) < abs(cr.game.gravity*0.5):
                self.remaining_jump_power = 0
                self.is_jumping = False
                self.is_falling = True


    def check_movements( self ):
        h_keys = cr.event_holder.held_keys
        p_keys = cr.event_holder.pressed_keys
        r_keys = cr.event_holder.released_keys
        if K_RIGHT in h_keys:
            self.move(Vector2(self.move_speed,0))

        if K_LEFT in h_keys:
            self.move(Vector2(-self.move_speed, 0))


        if K_SPACE in p_keys:
            self.jump_power = self.min_jump_power




        if K_SPACE in h_keys and abs(self.jump_power) < abs(self.max_jump_power) :
            self.is_charging = True
            self.jump_power += self.jump_power_per_second
            if abs(self.jump_power) > abs(self.max_jump_power):
                self.jump_power = self.max_jump_power

        if K_SPACE in r_keys:
            self.is_charging = False
            self.jump_request()

    def check_events( self ) :
        self.check_movements()
        self.check_jump()
        self.gravity_tick()
        self.manage_shake_particles()
        self.manage_jump_particles()
        self.manage_fall_particles()
        for particle in self.particles:
            particle.check_events()
        super(Player, self).check_events()
        self.is_moving = False


    def render_debug( self ) :
        pg.draw.rect(cr.screen, "purple", self.rect)


    def render( self ) :
        if cr.event_holder.should_render_debug :
            self.render_debug()

        for particle in self.particles:
            particle.render()

        pg.draw.polygon(cr.screen, self.color, self.points)
        # pg.draw.polygon(cr.screen, self.color.lerp("red",0.5), self.original_points)

        pg.draw.polygon(cr.screen, self.border_color, self.points, width=self.border_size)

        self.face.render()



    def add_particle( self,source:Vector2,angle,size ):
        self.particles.append(Particle(source, size, angle))
        if len(self.particles) > self.maximum_particles :
            self.particles.pop(0)


    def manage_movement_particles( self,value ):
        angle = random.randint(30, 60)

        if value.x > 0 :
            angle = - angle

        size = random.uniform(1, 4)

        self.add_particle(Vector2(self.center),angle,size)


    def manage_shake_particles( self ):
        if not self.is_shaking:
            return


        angle = random.randint(15, 60)
        if random.randint(0,1) :
            angle = - angle

        size = random.uniform(1, 4)

        self.add_particle(Vector2(self.center),angle,size)

    def manage_jump_particles( self ):
        if not self.is_jumping:
            return

        angle = random.randint(135,225)
        if random.randint(0, 1) :
            angle = - angle

        size = random.uniform(1, 4)

        self.add_particle(Vector2(self.center), angle, size)


    def manage_fall_particles( self ) :
        if not self.is_falling :
            return

        angle = random.randint(-45, 45)
        if random.randint(0, 1) :
            angle = - angle

        size = random.uniform(1, 4)

        self.add_particle(Vector2(self.center), angle, size)