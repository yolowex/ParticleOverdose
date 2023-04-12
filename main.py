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

# cr.screen = pg.display.set_mode([900, 640], SCALED | FULLSCREEN)
cr.screen = pg.display.set_mode([900,640], SCALED | FULLSCREEN)
cr.event_holder = EventHolder()
cr.event_holder.should_render_debug = False
cr.event_holder.determined_fps = 1000
cr.game = Game()
cr.game.init()

font = pg.font.SysFont('monospace', 30)
fps_text = lambda : font.render(f"FPS :{int(cr.event_holder.final_fps)}", True, "white")

while not cr.event_holder.should_quit :
    if K_F3 in cr.event_holder.pressed_keys :
        cr.event_holder.should_render_debug = not cr.event_holder.should_render_debug

    cr.event_holder.get_events()
    cr.game.check_events()
    cr.game.render()



    p = cr.game.player.center.copy()
    p.x = -int(p.x) + int(cr.screen.get_width() * .5)
    p.y = -int(p.y) + int(cr.screen.get_height() * .8)

    cr.camera.pos = p
    # cr.surface.scroll(-int(p.x) + int(cr.surface.get_width() * .5),

    if cr.event_holder.should_render_debug :
        cr.screen.blit(fps_text(), (0, 0))

    pg.display.update()

    # pg.image.save(cr.screen, "./dump.jpg")
