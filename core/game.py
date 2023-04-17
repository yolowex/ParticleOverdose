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
        self.timer = now()
        self.camera_x_offset = 0
        self.camera_y_offset = 0

        s = cr.screen.get_size()
        # experimental

        self.level = Level()
        self.inventory = Inventory()

        p_rect = FRect(0, 0, 0, 0)
        p_rect.w, p_rect.h = self.level.player_size
        p_rect.center = Vector2(self.level.player_pos)
        self.player = Player(rect_convert_polygon(p_rect))
        self.particles = []
        self.maximum_particles = 1000
        if IS_WEB :
            self.maximum_particles = 1000
        self.gravity = 500

        p = self.player.center.copy()
        p.x = -int(p.x) + int(cr.screen.get_width() * 0.5)
        p.y = -int(p.y) + int(cr.screen.get_height() * 0.8)

        cr.camera.pos = p


    def reset_player( self, new_game: bool = False ) :
        l_locked = self.player.locked_swords_list
        l_diamonds = self.player.acquired_diamonds
        l_lives = self.player.lives

        p_rect = FRect(0, 0, 0, 0)
        p_rect.w, p_rect.h = self.level.player_size
        p_rect.center = Vector2(self.level.player_pos)
        self.player = Player(rect_convert_polygon(p_rect))
        self.player.init()

        if not new_game :
            self.player.locked_swords_list = l_locked
            self.player.acquired_diamonds = l_diamonds
            self.player.lives = l_lives


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

        x = (self.player.sword.is_attacking and self.player.sword.name in ['light', 'evil'])

        go_center = self.player.is_jumping or \
                    (x and self.player.sword.attack_key == ATTACK_SPECIAL) or self.player.is_falling

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

        if K_s in h_keys or go_center :
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


    @property
    def inner_box_list( self ) :
        return cr.inner_box_list


    @property
    def diamonds_text( self ) :
        return cr.font.render(
            f"Diamonds: {self.player.acquired_diamonds}/{self.level.total_diamonds}", False,
            "black")


    @property
    def time_text( self ) :
        return cr.font.render(f"{round(pg.time.get_ticks() / 1000 - self.timer, 1)}".zfill(5),
            False, (155, 0, 0))


    @property
    def lives_text( self ) :
        return cr.font.render(f"lives: {self.player.lives}/{self.player.max_lives}", False,
            (0, 55, 0))


    def check_dead_player( self ) :
        if K_p in cr.event_holder.released_keys or K_LCTRL in cr.event_holder.released_keys :
            self.reset_player()


    def check_events( self ) :
        cr.inner_box_list = self.level.inner_box_list
        gravity = self.gravity
        gravity *= cr.event_holder.delta_time
        self.level.check_events()
        self.player.gravity_request(gravity)

        if not self.player.is_dead :
            self.player.check_events()
        else :
            self.check_dead_player()

        self.inventory.check_events()
        self.check_particles()
        self.check_camera_and_peek()


    @property
    def dead_player_text( self ) :
        return cr.font.render("You are dead, press P to respawn!", True, "red")


    def render_dead_player_text( self ) :
        if self.player.lives == 0 :
            return

        surface = self.dead_player_text
        rect = surface.get_rect()
        rect.center = cr.screen.get_rect().center
        cr.screen.blit(surface, rect)


    def render( self ) :
        cr.screen.fill(self.bg)

        self.level.render()
        self.inventory.render()

        self.player.render()
        if self.player.is_dead :
            self.render_dead_player_text()

        text = self.diamonds_text
        rect = text.get_rect()
        rect.x = cr.screen.get_width() - rect.w
        cr.screen.blit(text, rect)

        time_text = self.time_text
        time_rect = time_text.get_rect()
        time_rect.x = cr.screen.get_width() - time_rect.w
        time_rect.y += rect.h * 1.3
        cr.screen.blit(time_text, time_rect)

        lives_text = self.lives_text
        lives_rect = lives_text.get_rect()
        lives_rect.x = cr.screen.get_width() - lives_rect.w
        lives_rect.y += time_rect.y + time_rect.h * 1.3
        cr.screen.blit(lives_text, lives_rect)
