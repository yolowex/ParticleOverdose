from core.common_names import *
import core.common_resources as cr
from core.constants import *
from core.jelly_cube import JellyCube
from core.particle import Particle
from core.face import Face
from core.common_functions import *
from core.sword import Sword


class Player(JellyCube) :

    def __init__( self, points: list[Vector2] ) :
        self.color = WHITE
        self.border_color = BLACK.lerp(WHITE, 0.5)
        self.border_size = 1
        if self.border_size < 1 :
            self.border_size = 1

        self.face = Face()
        self.sword = Sword()
        self.move_speed = 300
        self.gravity = 0
        self.jump_power = 0

        self.max_jump_power = -2500
        self.min_jump_power = -1000
        self.remaining_jump_power = 0

        self.maximum_particles = 500
        self.particles = []
        # This is calculated only after a particle becomes inactive
        self.particles_age = 4
        self.facing = RIGHT

        super(Player, self).__init__(points)


    def init( self ) :
        self.face.init()
        self.sword.init()


    @property
    def jump_power_per_second( self ) :
        return self.min_jump_power * cr.event_holder.delta_time


    def gravity_tick( self ) :
        last_center = self.center
        center = last_center.copy()

        center.y += self.gravity
        self.gravity = 0
        self.center = center

        any_ = False
        for box in cr.game.inner_box_list :
            if box.colliderect(self.rect) :
                any_ = True

        if any_ :
            self.center = last_center
            self.is_falling = False


    def gravity_request( self, gravity: float ) :
        self.gravity = gravity
        for particle in self.particles :
            particle.gravity_request(gravity)


    def move( self, value: Vector2 ) :

        throw = (self.sword.last_attack_type in THROW_TYPES and (self.sword.is_attacking
                                or self.sword.is_retrieving))

        if value.x < 0 and not throw  :
            self.facing = LEFT
        elif value.x > 0 and not throw :
            self.facing = RIGHT
        else :
            return

        self.manage_movement_particles(value)
        last_center = self.center
        center = last_center.copy()
        center.x += value.x * cr.event_holder.delta_time
        center.y += value.y * cr.event_holder.delta_time
        self.center = center

        any_ = False
        for box in cr.game.inner_box_list :
            if box.colliderect(self.rect) :
                any_ = True

        if any_ :
            self.center = last_center
        else :
            self.is_moving = True
            super(Player, self).move(value)


    def jump_request( self ) :
        self.is_jumping = True
        self.remaining_jump_power = self.jump_power


    def check_jump( self ) :
        last_center = self.center
        center = last_center.copy()
        center.y += self.remaining_jump_power * cr.event_holder.delta_time
        self.center = center

        any_ = False
        for box in cr.game.inner_box_list :
            if box.colliderect(self.rect) :
                any_ = True

        if any_ :
            self.center = last_center
            self.remaining_jump_power = 0
            self.is_jumping = False
            self.is_falling = True
        else :
            self.remaining_jump_power -= (
                    self.remaining_jump_power * 7 * cr.event_holder.delta_time)
            if abs(self.remaining_jump_power) < abs(cr.game.gravity * 0.5) :
                self.remaining_jump_power = 0

            if abs(self.remaining_jump_power) < abs(cr.game.gravity * 1) :
                self.is_jumping = False
                self.is_falling = True


    def check_movements( self ) :
        h_keys = cr.event_holder.held_keys
        p_keys = cr.event_holder.pressed_keys
        r_keys = cr.event_holder.released_keys
        if K_RIGHT in h_keys :
            self.move(Vector2(self.move_speed, 0))

        if K_LEFT in h_keys :
            self.move(Vector2(-self.move_speed, 0))

        if K_SPACE in p_keys :
            self.jump_power = self.min_jump_power

        if K_SPACE in h_keys and abs(self.jump_power) < abs(self.max_jump_power) :
            self.is_charging = True

            self.jump_power += self.jump_power_per_second
            if abs(self.jump_power) > abs(self.max_jump_power) :
                self.jump_power = self.max_jump_power

        if K_SPACE in r_keys :
            self.is_charging = False
            self.jump_request()


    def dev_sword_control( self ) :
        p_keys = cr.event_holder.pressed_keys
        if K_1 in p_keys :
            self.sword.update_sword('evil')
        if K_2 in p_keys :
            self.sword.update_sword('desire')
        if K_3 in p_keys :
            self.sword.update_sword('light')
        if K_4 in p_keys :
            self.sword.update_sword('hawk')
        if K_5 in p_keys :
            self.sword.update_sword('blood')
        if K_6 in p_keys :
            self.sword.update_sword('death')


    def check_events( self ) :
        self.check_movements()
        self.check_jump()
        self.gravity_tick()
        self.manage_shake_particles()
        self.manage_jump_particles()
        self.manage_fall_particles()
        self.update_face()
        self.dev_sword_control()
        self.sword.check_events()

        for particle, c in zip(self.particles[: :-1], range(len(self.particles))[: :-1]) :
            if particle.destroy_time is not None :
                if particle.destroy_time + particle.age < now() :
                    self.particles.pop(c)

            elif particle.init_time + particle.absolute_age < now() :
                self.particles.pop(c)

            particle.check_events()

        super(Player, self).check_events()
        if not self.is_still:
            self.sword.rotate_sword()

        self.is_moving = False


    def render_debug( self ) :
        rect = self.rect
        rect.x += cr.camera.x
        rect.y += cr.camera.y
        pg.draw.rect(cr.screen, "purple", rect)


    def render( self ) :
        if cr.event_holder.should_render_debug :
            self.render_debug()

        for particle in self.particles :
            particle.render()

        p = [i.copy() for i in self.points]
        move_points(p, cr.camera.x, cr.camera.y)

        pg.draw.polygon(cr.screen, self.color, p)
        # pg.draw.polygon(cr.screen, self.color.lerp("red",0.5), self.original_points)

        pg.draw.polygon(cr.screen, self.border_color, p, width=self.border_size)

        self.face.render()
        self.sword.render()


    def add_particle( self, source: Vector2, angle, size ) :
        if len(self.particles) > self.maximum_particles :
            return

        age = random.uniform(0, 1)
        self.particles.append(Particle(source, size, angle, age))


    def manage_movement_particles( self, value ) :
        angle = random.randint(30, 60)

        if value.x > 0 :
            angle = - angle

        size = random.uniform(1, 4)

        self.add_particle(Vector2(self.center), angle, size)


    def manage_shake_particles( self ) :
        if not self.is_shaking :
            return

        angle = random.randint(15, 60)
        if random.randint(0, 1) :
            angle = - angle

        size = random.uniform(1, 4)

        self.add_particle(Vector2(self.center), angle, size)


    def manage_jump_particles( self ) :
        if not self.is_jumping :
            return

        angle = random.randint(135, 225)
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


    def update_face( self ) :
        if self.is_charging :
            self.face.update_face(new_eye="silly", new_mouth="talk_1")
        elif self.is_falling :
            self.face.update_face(new_eye="jump", new_mouth="talk_3")
        elif self.is_moving :
            self.face.update_face(new_eye="angry", new_mouth="smirk_1")
        elif self.is_shaking and not self.is_jumping :
            self.face.update_face(new_eye="dead", new_mouth="hoo_hoo")
        elif not self.is_moving :
            self.face.update_face(new_eye="angry", new_mouth="smirk_0")
