import pygame as pg
from pygame.locals import *
import numpy
from PIL import Image

from core.event_holder import EventHolder
import core.common_resources as cr
from core.game import Game
from core.constants import *
from core.sprite import Sprite
from core.common_names import *
from core.common_functions import *

pic = "./pic.png"
res = "./pic_res.png"

pg.init()

cr.screen = pg.display.set_mode([800,640],SCALED | FULLSCREEN)
cr.event_holder = EventHolder()
cr.event_holder.should_render_debug = False
cr.event_holder.determined_fps = 1000
cr.game = Game()

sprite = Sprite("./26.jpeg")
rect = sprite.transformed_surface.get_rect()
points = rect_convert_polygon(rect)


def update():
    sprite.transform_by_points(points,cr.game.player.rect)

font = pg.font.SysFont("monospace",15)

def fps_text():
    text = f"FPS: {round(cr.event_holder.final_fps)}"
    return font.render(text,False,"white")

while not cr.event_holder.should_quit:
    if K_F3 in cr.event_holder.pressed_keys:
        cr.event_holder.should_render_debug = not cr.event_holder.should_render_debug

    h_keys = cr.event_holder.held_keys

    if K_UP in h_keys:
        points[0].y -= 5
        update()

    if K_DOWN in h_keys:
        points[0].y += 5
        update()


    cr.event_holder.get_events()
    cr.screen.fill(WHITE)

    rect = sprite.transformed_surface.get_rect()
    rect.center = cr.screen.get_rect().center
    cr.screen.blit(sprite.transformed_surface,rect)

    cr.game.check_events()
    cr.game.render()
    if cr.event_holder.should_render_debug:
        cr.screen.blit(fps_text(),[0,0])


    pg.display.update()
