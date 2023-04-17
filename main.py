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
cr.little_font = pg.font.SysFont('Arial', 15)
cr.smallest_font = pg.font.SysFont('monospace', 10)

font = cr.font
last_time = 0


def game_over_text() :
    return cr.little_font.render(
        f"You found {last_diamonds} Diamonds in {last_time} seconds! Good Job! press X to replay", True,
        "red")


def win_text() :
    return cr.little_font.render(
        f"You gathered all Diamonds in {last_time} seconds! Very nice! press X to replay", True, "red")


pg.mouse.set_visible(False)

just_lost = False
just_won = False

last_diamonds = 0
async def main() :
    global last_time, just_lost, just_won
    global last_diamonds

    # cr.screen = pg.display.set_mode([900, 640], SCALED | FULLSCREEN)
    if IS_WEB :  # web only, scales automatically
        cr.screen = pg.display.set_mode([900 * 0.8, 640 * 0.8])
    else :
        cr.screen = pg.display.set_mode([900 * 0.8, 640 * 0.8], SCALED | FULLSCREEN)

    start_playing = False

    cr.event_holder = EventHolder()
    cr.event_holder.should_render_debug = False
    cr.event_holder.determined_fps = 1000

    start_playing_text = font.render("press P to start Playing!", True, "red")


    def reset_game() :
        start_playing = False
        cr.world = json.loads(open(levels_root + "test.json").read())
        cr.game = Game()
        cr.game.init()


    reset_game()

    this_font = cr.smallest_font
    if IS_WEB:
        this_font = cr.little_font

    fps_text = lambda : this_font.render(f"FPS :{int(cr.event_holder.final_fps)}"
                                              f" PARTICLES: {cr.game.player.particles.__len__()}",
        True, "white")

    wait_text = this_font.render("Please wait while loading...",True,"red")

    # I F**king love OOP :heart:
    while not cr.event_holder.should_quit :
        if cr.game.player.lives == 0 and not just_lost :
            last_time = round(now() - cr.game.timer, 2)
            last_diamonds = cr.game.player.acquired_diamonds
            reset_game()
            just_lost = True

        if cr.game.player.acquired_diamonds == cr.game.level.total_diamonds and not just_won :
            last_diamonds = cr.game.player.acquired_diamonds
            last_time = round(now() - cr.game.timer, 2)

            reset_game()
            just_won = True

        if K_F3 in cr.event_holder.pressed_keys :
            cr.event_holder.should_render_debug = not cr.event_holder.should_render_debug

        if K_x in cr.event_holder.released_keys :
            if just_won or just_lost :
                just_lost = False
                just_won = False

        if K_F12 in cr.event_holder.released_keys:
            just_lost = False
            just_won = False

        cr.event_holder.get_events()
        if IS_WEB and cr.event_holder.should_quit:
            cr.event_holder.should_quit = False



        win_focus = cr.event_holder.window_focus and cr.event_holder.focus_gain_timer + 1 < now()
        mouse_focus = cr.event_holder.mouse_focus and cr.event_holder.mouse_focus_gain_timer + 1 < now()

        should = start_playing and not (just_lost or just_won) and (win_focus and mouse_focus)


        if not should:
            cr.screen.fill([0,0,0,0])
        if should:
            cr.game.check_events()
            cr.game.render()

        if not should and not just_lost and not just_won:
            rect = wait_text.get_rect()
            rect.center = cr.screen.get_rect().center
            rect.y = cr.screen.get_height() * 0.7
            cr.screen.blit(wait_text,rect)

        if not start_playing :
            text_rect = start_playing_text.get_rect()
            text_rect.center = cr.screen.get_rect().center
            cr.screen.blit(start_playing_text, text_rect)
            if K_p in cr.event_holder.released_keys or K_LCTRL in cr.event_holder.released_keys :
                start_playing = True
                just_lost = False
                cr.game.timer = now()

        text = fps_text()
        cr.screen.blit(fps_text(),
            (cr.screen.get_width() - text.get_width(), cr.screen.get_height() - text.get_height()))

        if just_lost :
            surface = game_over_text()
            rect = surface.get_rect()
            rect.center = cr.screen.get_rect().center
            cr.screen.blit(surface, rect)

        if just_won :
            surface = win_text()
            rect = surface.get_rect()
            rect.center = cr.screen.get_rect().center
            cr.screen.blit(surface, rect)

        pg.display.update()

        # pg.image.save(cr.screen, "./dump.jpg")

        await asyncio.sleep(0)


if __name__ == '__main__' :
    asyncio.run(main())
