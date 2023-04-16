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
        self.init_points = points.copy()

        self.color = WHITE
        self.border_color = BLACK.lerp(WHITE, 0.5)
        self.lives = 5
        self.max_lives = 5
        self.border_size = 1
        if self.border_size < 1 :
            self.border_size = 1

        self.is_dead = False
        self.locked_swords_list = ['hawk','light','desire','death','evil']
        self.acquired_diamonds = 0

        self.anti_gravity = False
        self.face = Face()
        self.sword = Sword()
        self.move_speed = 300
        self.gravity = 0
        self.jump_power = 0
        self.did_jump = False
        self.max_jump_power = -2500
        self.min_jump_power = -1000
        self.remaining_jump_power = 0
        self.is_wet = False
        self.on_fire = False

        # This is calculated only after a particle becomes inactive
        self.particles_age = 4
        self.facing = RIGHT
        self.movement_request = Vector2(0, 0)

        super(Player, self).__init__(points)

    @property
    def is_flying( self ):
        return self.sword.name == 'evil' and self.sword.is_attacking

    @property
    def particle_delta_count( self ) :
        delta = cr.event_holder.delta_time
        if delta <= 0.01 :
            delta = 0.01
        count = int(delta * 200)
        return count


    @property
    def maximum_particles( self ) :
        return cr.game.maximum_particles


    @property
    def particles( self ) :
        return cr.game.particles


    def init( self ) :
        self.face.init()
        self.sword.init()


    @property
    def jump_power_per_second( self ) :
        return self.min_jump_power * cr.event_holder.delta_time


    def gravity_tick( self ) :
        if self.anti_gravity :
            return

        water_m = 1
        if self.is_wet or self.is_flying:
            water_m = 0.4



        movement = Vector2(0, self.gravity * water_m)
        any_ = self.is_colliding(movement)
        if not any_ :
            self.center = Vector2(self.center.x + movement.x, self.center.y + movement.y)
        else :
            c = self.center
            # c.y = (any_.y - self.o_rect.h / 2 ) - 0
            self.center = c
            self.is_falling = False
            self.did_jump = False

        self.gravity = 0


    def check_lava( self ) -> bool:
        self.on_fire = False
        for lavabox in cr.game.level.lava_colliders_list :
            if self.rect.colliderect(lavabox) :
                if self.sword.name != 'desire':
                    self.kill()
                    self.face.update_face(new_eye="dead",new_mouth="talk_1")
                    # Bad programming
                    return True
                self.on_fire = True

        return False

    def gravity_request( self, gravity: float ) :
        self.gravity = gravity
        for particle in self.particles :
            particle.gravity_request(gravity)

    def kill( self ):
        self.lives -= 1
        self.is_dead = True

    def move( self, value: Vector2, anti_gravity: bool = False ) :
        self.anti_gravity = anti_gravity
        if self.anti_gravity :
            self.is_falling = False

        water_m = 1

        if self.sword.name == 'evil':
            water_m = 1.4
        if self.sword.name == 'desire':
            water_m = 1
        if self.is_flying:
            water_m = 1

        if value.y < 0: # above
            water_m *= 2
            if self.is_jumping:
                water_m = 0

        if value.y > 0: # below
            water_m *= 0.3



        throw = (self.sword.last_attack_type in THROW_TYPES and (
                self.sword.is_attacking or self.sword.is_retrieving))

        if value.x < 0 and not throw :
            self.facing = LEFT
        elif value.x > 0 and not throw :
            self.facing = RIGHT

        self.manage_movement_particles(value)
        movement = Vector2(value.x * water_m * cr.event_holder.delta_time,
            value.y * water_m * cr.event_holder.delta_time)
        any_ = self.is_colliding(movement)

        if any_ :
            return False
        else :
            c = self.center
            c.x += movement.x
            c.y += movement.y
            self.center = c

            self.is_moving = True
            super(Player, self).move(value)
            return True


    def jump_request( self ) :
        self.is_jumping = True
        self.remaining_jump_power = self.jump_power


    def check_color_update( self ) :
        if self.is_shaking :
            new_color = random_color()
            val = cr.event_holder.delta_time * 15
            if val > 0.10 :
                val = 0.10

            self.color = self.color.lerp(new_color, val)

        else :
            base_color = WHITE
            if self.sword.name == 'blood' :
                base_color = RED
            elif self.sword.name == 'light' :
                base_color = Color(255, 255, 0)
            elif self.sword.name == 'evil' :
                base_color = Color(0, 255, 0)
            elif self.sword.name == 'death' :
                base_color = Color("black")
            elif self.sword.name == 'desire' :
                base_color = Color(255, 155, 0)
            elif self.sword.name == 'hawk' :
                base_color = Color(0, 0, 255)

            lerp_value = cr.event_holder.delta_time * 2.5
            if lerp_value > 1 :
                lerp_value = 1
            self.color = self.color.lerp(base_color, lerp_value)


    def check_jump( self ) :
        water_m = 1
        if self.is_wet :
            water_m = 0.5

            if self.sword.name == 'evil' :
                water_m = 2

        last_center = self.center
        movement = Vector2(0, self.remaining_jump_power * water_m * cr.event_holder.delta_time)
        any_ = self.is_colliding(movement)

        if any_ :
            self.center = last_center
            self.remaining_jump_power = 0
            self.is_jumping = False
            self.is_falling = True
        else :
            c = self.center
            c.x += movement.x
            c.y += movement.y
            self.center = c
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

        if self.anti_gravity :
            return

        if K_RIGHT in h_keys :
            self.move(Vector2(self.move_speed, 0))

        if K_LEFT in h_keys :
            self.move(Vector2(-self.move_speed, 0))

        if self.is_wet or self.on_fire or self.is_flying :
            if K_DOWN in h_keys :
                self.move(Vector2(0, self.move_speed))
            if K_UP in h_keys :
                self.move(Vector2(0, -self.move_speed))



        if not self.did_jump :
            if K_SPACE in p_keys :
                self.jump_power = self.min_jump_power
                self.is_charging = True

            if self.is_charging :
                if K_SPACE in h_keys and abs(self.jump_power) < abs(self.max_jump_power) :
                    self.jump_power += self.jump_power_per_second
                    if abs(self.jump_power) > abs(self.max_jump_power) :
                        self.jump_power = self.max_jump_power

                if K_SPACE in r_keys :
                    self.did_jump = True
                    self.is_charging = False
                    self.jump_request()


    def dev_sword_control( self ) :
        cant_do = self.sword.is_attacking or self.sword.is_retrieving

        p_keys = cr.event_holder.pressed_keys
        if not cant_do :
            if K_1 in p_keys and 'evil' not in self.locked_swords_list :
                self.sword.update_sword('evil')
            if K_2 in p_keys and 'desire' not in self.locked_swords_list :
                self.sword.update_sword('desire')
            if K_3 in p_keys and 'light' not in self.locked_swords_list :
                self.sword.update_sword('light')
            if K_4 in p_keys and 'hawk' not in self.locked_swords_list :
                self.sword.update_sword('hawk')
            if K_5 in p_keys and 'blood' not in self.locked_swords_list :
                self.sword.update_sword('blood')
            if K_6 in p_keys and 'death' not in self.locked_swords_list :
                self.sword.update_sword('death')


    def is_colliding( self, movement: Vector2 ) -> FRect or bool :
        n_rect = self.o_rect
        n_rect.x += movement.x
        n_rect.y += movement.y

        any_: Optional[FRect, bool] = False
        for box in cr.game.inner_box_list :
            if box.colliderect(n_rect) :
                any_ = box
                break

        return any_

    @property
    def jump_power_percent( self ):
        return percent(abs(self.max_jump_power) - abs(self.min_jump_power),
            abs(self.jump_power) - abs(self.min_jump_power))

    def check_events( self ) :
        if self.center.y > cr.game.level.lowest_tile + 500:
            self.kill()
            self.face.update_face(new_eye="dead", new_mouth="talk_1")
            return

        self.is_wet = False
        for waterbox in cr.game.level.water_colliders_list :
            if self.rect.colliderect(waterbox) :
                self.is_wet = True
                break

        if self.check_lava():
            return

        self.check_movements()
        self.check_jump()
        self.gravity_tick()
        self.manage_shake_particles()
        self.manage_jump_particles()
        self.manage_fall_particles()
        self.update_face()
        self.dev_sword_control()
        self.check_color_update()
        self.anti_gravity = False
        self.sword.check_events()

        super(Player, self).check_events()
        if not self.is_still :
            self.sword.rotate_sword()

        self.is_moving = False


    def render_debug( self ) :
        rect = self.rect
        rect.x += cr.camera.x
        rect.y += cr.camera.y
        pg.draw.rect(cr.screen, "purple", rect)

        o_rect = self.o_rect
        o_rect.x += cr.camera.x
        o_rect.y += cr.camera.y
        pg.draw.rect(cr.screen, "yellow", o_rect)


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


        if self.is_charging:
            color = 'green'
            rect = self.rect
            rect.w = rect.w * 0.2
            rect.x -= rect.w * 1.3
            lh = rect.h
            rect.h = rect.h * self.jump_power_percent * 0.01
            rect.y += lh - rect.h

            rect.x += cr.camera.x
            rect.y += cr.camera.y

            if self.facing == LEFT:
                rect.x += self.rect.w * 1.3 + (rect.w)

            pg.draw.rect(cr.screen,color,rect)




        self.face.render()
        self.sword.render()


    def add_particle( self, source: Vector2, angle, size ) :
        # return

        if len(self.particles) > self.maximum_particles :
            return

        age = random.uniform(0, 1)

        anti_gravity = anti_collision = False
        if IS_WEB :
            anti_gravity = anti_collision = True

        particle = Particle(source, size, angle, age, None, anti_gravity, anti_collision)

        particle.power = 10
        if IS_WEB :
            particle.power = 3  # particle.power += random.uniform(particle.power*-0.8,particle.power)

        particle.power_decrease_scale = 2
        if self.is_wet :
            particle.power_decrease_scale *= 6

        self.particles.append(particle)


    def manage_movement_particles( self, value ) :
        for _ in range(self.particle_delta_count) :
            angle = random.randint(30, 60)

            if value.x > 0 :
                angle = - angle

            size = random.uniform(1, 4)

            self.add_particle(Vector2(self.center), angle, size)


    def manage_shake_particles( self ) :
        if not self.is_shaking :
            return
        for _ in range(self.particle_delta_count) :
            angle = random.randint(15, 60)
            if random.randint(0, 1) :
                angle = - angle

            size = random.uniform(1, 4)

            self.add_particle(Vector2(self.center), angle, size)


    def manage_jump_particles( self ) :
        if not self.is_jumping :
            return
        for _ in range(self.particle_delta_count) :
            angle = random.randint(135, 225)
            if random.randint(0, 1) :
                angle = - angle

            size = random.uniform(1, 4)

            self.add_particle(Vector2(self.center), angle, size)


    def teleport( self, to: Vector2 ) :
        l_center = self.center
        self.center = to
        if self.is_colliding(Vector2(0, 0)) :
            self.center = l_center
            print("Could not teleport, invalid location.")


    def manage_fall_particles( self ) :
        if not self.is_falling :
            return

        for _ in range(self.particle_delta_count) :
            angle = random.randint(-45, 45)
            if random.randint(0, 1) :
                angle = - angle

            size = random.uniform(1, 4)

            self.add_particle(Vector2(self.center), angle, size)


    def update_face( self ) :
        new_eye = None
        new_mouth = None
        # EYES
        if self.is_charging :
            new_eye = 'silly'
        elif self.is_falling :
            new_eye = "jump"
        elif self.is_moving :
            new_eye = "angry"
        elif self.is_shaking and not self.is_jumping :
            new_eye = "dead"
        elif not self.is_moving :
            new_eye = "angry"

        # MOUTH

        if self.is_charging :
            new_mouth = "talk_1"
        elif self.is_falling :
            new_mouth = "talk_3"
        elif self.is_moving :
            new_mouth = "smirk_1"
        elif self.is_shaking and not self.is_jumping :
            new_mouth = "hoo_hoo"
        elif not self.is_moving :
            new_mouth = "smirk_0"

        # SWORD

        if self.sword.is_active and not self.sword.is_attacking and self.sword.attack_key == ATTACK_SPECIAL and self.is_still :
            new_mouth = 'smile'

        if self.sword.is_attacking :
            if self.sword.name == 'light' :
                if self.sword.attack_key == ATTACK_SPECIAL :
                    new_eye = 'love'
                    new_mouth = 'hoo_hoo'

            if self.sword.name == 'blood' :
                new_eye = 'rage'

            if self.sword.name == 'desire' :
                if self.sword.attack_key == ATTACK_SPECIAL :
                    new_eye = 'rage'
                    new_mouth = 'smirk_0'

        if self.is_still or self.is_moving :
            if self.sword.name == 'blood' :
                new_eye = 'rage'

        if self.sword.was_thrown :
            new_mouth = 'smile'
            if self.sword.name == 'desire' :
                new_mouth = 'smirk_1'

        self.face.update_face(new_eye, new_mouth)
