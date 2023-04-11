import pygame as pg
from pygame.locals import *
import numpy
from PIL import Image

from core.event_holder import EventHolder
import core.common_resources as cr
from core.game import Game
from core.constants import *
from core.sprite import Sprite

pic = "./pic.png"
res = "./pic_res.png"


sprite = Sprite(pic)

cr.screen = pg.display.set_mode([800,640],SCALED | FULLSCREEN)
cr.event_holder = EventHolder()
cr.event_holder.determined_fps = 60
cr.game = Game()
pg.init()
clock = pg.time.Clock()


selected_point = 0



while not cr.event_holder.should_quit:

    p_keys = cr.event_holder.pressed_keys
    h_keys = cr.event_holder.held_keys
    if K_1 in p_keys:
        selected_point = 0
    if K_2 in p_keys:
        selected_point = 1
    if K_3 in p_keys:
        selected_point = 2
    if K_4 in p_keys:
        selected_point = 3


    if K_UP in h_keys:
        sprite.r0[selected_point][1] -= 2
        sprite.update()

    if K_DOWN in h_keys:
        sprite.r0[selected_point][1] += 2
        sprite.update()

    if K_RIGHT in h_keys:
        sprite.r0[selected_point][0] += 2
        sprite.update()

    if K_LEFT in h_keys:
        sprite.r0[selected_point][0] -= 2
        sprite.update()

    cr.event_holder.get_events()
    # cr.game.check_events()
    # cr.game.render()
    cr.screen.fill(WHITE.lerp(BLACK,0.3))

    s_rect = sprite.transformed_surface.get_rect()
    s_rect.center = cr.screen.get_rect().center

    # pg.draw.polygon(cr.screen,RED,r0,width=1)
    # pg.draw.polygon(cr.screen,BLACK,r1,width=1)

    cr.screen.blit(sprite.transformed_surface,s_rect)

    pg.display.update()
    clock.tick(cr.event_holder.determined_fps)