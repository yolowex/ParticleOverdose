import pygame as pg
from pygame.locals import *


from core.event_holder import EventHolder
import core.common_resources as cr
from core.game import Game



cr.screen = pg.display.set_mode([800,640],SCALED | FULLSCREEN)
cr.event_holder = EventHolder()
cr.game = Game()
pg.init()

while not cr.event_holder.should_quit:
    cr.event_holder.get_events()
    cr.game.check_events()
    cr.game.render()
    pg.display.update()