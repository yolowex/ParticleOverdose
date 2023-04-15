import pygame as pg
from pygame.locals import *

from core.event_holder import EventHolder
import core.common_resources as cr
from core.game import Game
from core.constants import *
from core.common_functions import *
import core.constants as const
import asyncio

pic = "./pic.png"
res = "./pic_res.png"

pg.init()

cr.font = pg.font.SysFont('monospace', 20)
font = cr.font

pg.mouse.set_visible(False)
async def main():
    # cr.screen = pg.display.set_mode([900, 640], SCALED | FULLSCREEN)
    if IS_WEB: # web only, scales automatically
        cr.screen = pg.display.set_mode([900*0.6,640*0.6])
    else:
        cr.screen = pg.display.set_mode([900*0.6,640*0.6], SCALED | FULLSCREEN)

    start_playing = False

    cr.event_holder = EventHolder()
    cr.event_holder.should_render_debug = False
    cr.event_holder.determined_fps = 1000

    start_playing_text = font.render("press P to start Playing!",True,"red")

    def reset_game():
        cr.world = json.loads(open(levels_root+"test.json").read())
        cr.game = Game()
        cr.game.init()

    reset_game()

    fps_text = lambda : font.render(f"FPS :{int(cr.event_holder.final_fps)}"
                            f" PARTICLES: {cr.game.player.particles.__len__()}", True, "white")

    # I F**king love OOP :heart:
    while not cr.event_holder.should_quit :
        if K_F3 in cr.event_holder.pressed_keys :
            cr.event_holder.should_render_debug = not cr.event_holder.should_render_debug

        if K_x in cr.event_holder.released_keys:
            reset_game()

        cr.event_holder.get_events()
        if start_playing:
            cr.game.check_events()

        cr.game.render()
        if not start_playing:
            text_rect = start_playing_text.get_rect()
            text_rect.center = cr.screen.get_rect().center
            cr.screen.blit(start_playing_text,text_rect)
            if K_p in cr.event_holder.released_keys or K_LCTRL in cr.event_holder.released_keys:
                start_playing = True
                cr.game.timer = now()


        if cr.event_holder.should_render_debug :
            cr.screen.blit(fps_text(), (0, 0))

        pg.display.update()

        # pg.image.save(cr.screen, "./dump.jpg")

        await asyncio.sleep(0)


if __name__ == '__main__':
    asyncio.run(main())

