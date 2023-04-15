from core.common_names import *
from core.player import Player
import core.common_resources as cr
from core.common_functions import *
from core.constants import *
from core.level import Level
from core.inventory import Inventory


class Game :

    def __init__( self ) :
        self.bg = SKY

        self.camera_x_offset = 0
        self.camera_y_offset = 0

        s = cr.screen.get_size()
        # experimental
        self.box = FRect(s[0] * 0.1, s[1] * 0.1, s[0] * 0.8, s[1] * 0.8)
        self.box_width = int(s[0] * 0.01)
        if self.box_width < 1 :
            self.box_width = 1

        self.level = Level()
        self.inventory = Inventory()

        p_rect = FRect(0, 0, 0, 0)
        p_rect.w, p_rect.h = self.level.player_size
        p_rect.center = self.box.center
        self.player = Player(rect_convert_polygon(p_rect))
        self.particles = []
        self.maximum_particles = 1000
        if IS_WEB :
            self.maximum_particles = 1000
        self.player.center = Vector2(self.level.player_pos)
        self.gravity = 500


    def init( self ) :
        self.player.init()
        self.level.init()
        r_mouth = list(cr.right_mouth_sprite_dict.values())
        l_mouth = list(cr.left_mouth_sprite_dict.values())
        mouth = r_mouth + l_mouth
        for sprite in mouth :
            sprite.transform_by_width(self.player.rect.w * 0.5)
            if sprite in l_mouth :
                sprite.flip(flip_x=True)

        r_eye = list(cr.right_eye_sprite_dict.values())
        l_eye = list(cr.left_eye_sprite_dict.values())
        eye = r_eye + l_eye
        for sprite in eye :
            sprite.transform_by_width(self.player.rect.w * 0.5)
            if sprite in l_eye :
                sprite.flip(flip_x=True)

        for name, sprite in list(cr.right_sword_dict.items()) + list(cr.left_sword_dict.items()) :
            m = 1.5
            if name == 'blood' :
                m = 1.75
            elif name == 'death' :
                m = 2.25

            sprite.transform_by_height(self.player.rect.h * m)

        for sprite in cr.right_sword_dict.values() :
            sprite.flip(True)


    def check_camera_and_peek( self ) :
        x_offset = 0.5
        y_offset = 0.8

        h_keys = cr.event_holder.held_keys

        cam_unit = cr.event_holder.delta_time * 0.5
        cam_release_unit = (1 - cr.event_holder.delta_time * 2)
        if cam_release_unit < 0 :
            cam_release_unit = 0
        if cam_release_unit > 1 :
            cam_release_unit = 1

        if K_a in h_keys :
            self.camera_x_offset += cam_unit
        if K_d in h_keys :
            self.camera_x_offset -= cam_unit

        if K_s in h_keys :
            self.camera_y_offset -= cam_unit

        if any(i in h_keys for i in [K_a, K_d, K_s]) :
            if self.camera_x_offset > 0.3 :
                self.camera_x_offset = 0.3
            elif self.camera_x_offset < -0.2 :
                self.camera_x_offset = -0.2
            if self.camera_y_offset < -0.6 :
                self.camera_y_offset = -0.6


        else :
            self.camera_x_offset *= cam_release_unit
            self.camera_y_offset *= cam_release_unit

            if abs(self.camera_x_offset) < 0.001 :
                self.camera_x_offset = 0

            if abs(self.camera_y_offset) < 0.001 :
                self.camera_y_offset = 0

        p = cr.game.player.center.copy()
        p.x = -int(p.x) + int(cr.screen.get_width() * (x_offset + self.camera_x_offset))
        p.y = -int(p.y) + int(cr.screen.get_height() * (y_offset + self.camera_y_offset))

        cr.camera.pos = p


    def check_particles( self ) :
        for particle, c in zip(self.particles[: :-1], range(len(self.particles))[: :-1]) :
            if particle.destroy_time is not None :
                if particle.destroy_time + particle.age < now() :
                    self.particles.pop(c)

            elif particle.init_time + particle.absolute_age < now() :
                self.particles.pop(c)

            particle.check_events()


    # experimental
    # @property
    # def inner_box( self ) -> FRect:
    #
    #     rect = self.box.copy()
    #     rect.x+=self.box_width
    #     rect.y+=self.box_width
    #     rect.w-=self.box_width*2
    #     rect.h-=self.box_width*2
    #     return rect

    # experimental

    # Bad usage of words, box means collidable here
    @property
    def inner_box_list( self ) :
        return cr.inner_box_list


    @property
    def diamonds_text( self ) :
        return cr.font.render(
            f"Diamonds: {self.player.acquired_diamonds}/{self.level.total_diamonds}",False,"black")


    @property
    def time_text( self ):
        return cr.font.render(f"{round(pg.time.get_ticks()/1000,1)}".zfill(5),False,(155,0,0))


    def check_events( self ) :
        cr.inner_box_list = self.level.inner_box_list
        gravity = self.gravity
        gravity *= cr.event_holder.delta_time
        self.level.check_events()
        self.player.gravity_request(gravity)
        self.player.check_events()
        self.inventory.check_events()
        self.check_particles()
        self.check_camera_and_peek()


    def render( self ) :
        cr.screen.fill(self.bg)
        # pg.draw.rect(cr.surface,BLACK,self.box,width=self.box_width)
        # pg.draw.rect(cr.surface,BLACK.lerp(WHITE,0.9),self.inner_box)
        self.level.render()
        self.inventory.render()
        self.player.render()

        text = self.diamonds_text
        rect = text.get_rect()
        rect.x = cr.screen.get_width() - rect.w
        cr.screen.blit(text,rect)

        time_text = self.time_text
        time_rect = time_text.get_rect()
        time_rect.x = cr.screen.get_width() - time_rect.w
        time_rect.y += rect.h*1.3
        cr.screen.blit(time_text,time_rect)

