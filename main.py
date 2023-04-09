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


cr.screen = pg.display.set_mode([800,640],SCALED | FULLSCREEN)
cr.event_holder = EventHolder()
cr.event_holder.determined_fps = 60
cr.game = Game()
pg.init()
clock = pg.time.Clock()

def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)

src_img = Image.open(pic)

img:Optional[Image] = None

def to_surface(image:Image):
    mode = image.mode
    size = image.size
    data = image.tobytes()

    py_image = pg.image.fromstring(data, size, mode)
    return py_image

pg_img:Optional[Surface] = None


r0 = [ list(i) for i in [(50, 0), (256, 0), (256, 256), (0, 256)]]
r1 = [ list(i) for i in [(0, 0), (256, 0), (256, 256), (0, 256)]]

def keep_inside():
    min_x = 0
    min_y = 0
    for x,y in r0:
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y

    for v in r0:
        if min_x < 0:
            v[0]-=min_x
        if min_y < 0:
            v[1]-=min_y

def update():
    global img
    global pg_img
    img = src_img.copy()
    width, height = img.size
    m = -0.5
    xshift = abs(m) * width
    new_width = width + int(round(xshift))

    coeffs = find_coeffs(r0,r1)
    keep_inside()
    img = img.transform((int(width*1.5), int(height*1.5)), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    img.save(res)

    pg_img = to_surface(img)


update()

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
        r0[selected_point][1] -= 2
        update()

    if K_DOWN in h_keys:
        r0[selected_point][1] += 2
        update()

    if K_RIGHT in h_keys:
        r0[selected_point][0] += 2
        update()

    if K_LEFT in h_keys:
        r0[selected_point][0] -= 2
        update()

    cr.event_holder.get_events()
    # cr.game.check_events()
    # cr.game.render()
    cr.screen.fill(WHITE.lerp(BLACK,0.3))

    s_rect = pg_img.get_rect()
    s_rect.center = cr.screen.get_rect().center

    # pg.draw.polygon(cr.screen,RED,r0,width=1)
    # pg.draw.polygon(cr.screen,BLACK,r1,width=1)

    cr.screen.blit(pg_img,s_rect)

    pg.display.update()
    clock.tick(cr.event_holder.determined_fps)