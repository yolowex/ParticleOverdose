import pygame as pg
from pygame.locals import *
import numpy
from PIL import Image

from core.event_holder import EventHolder
import core.common_resources as cr
from core.game import Game
from core.constants import *

pic = "./pic.png"
res = "./pic_res.png"

pg.init()

cr.screen = pg.display.set_mode([800,640],SCALED | FULLSCREEN)
cr.event_holder = EventHolder()
cr.event_holder.should_render_debug = True
cr.event_holder.determined_fps = 10000
cr.game = Game()


while not cr.event_holder.should_quit:


    cr.event_holder.get_events()
    cr.game.check_events()
    cr.game.render()

    pg.display.update()
