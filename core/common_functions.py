from core.common_names import *


def rect_convert_polygon( rect: FRect ) :
    return [Vector2(i) for i in
        [[rect.x, rect.y], [rect.x + rect.w, rect.y], [rect.x + rect.w, rect.y + rect.h],
            [rect.x , rect.y + rect.h],]]


def move_points(points:list[Vector2],x=0,y=0):
    for point in points:
        point.x += x
        point.y += y


def rotate_point(origin, point, angle):
    angle = math.radians(angle)
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return Vector2(qx, qy)


def percent(All,part):
    return (100/All) * part

def random_color() -> Color:
    return Color([random.randint(0,255) for _ in range(3)])

def now():
    return pg.time.get_ticks() / 1000


def get_rotated_points(rect:FRect,angle:float) -> list[Vector2]:

    l_min_x = rect.x
    l_min_y = rect.y

    res = []
    points = rect_convert_polygon(rect)
    c = Vector2(rect.center)

    for point in points:
        new_point = rotate_point(c,point,angle)
        res.append(new_point)

    min_x = min([i.x for i in res])
    min_y = min([i.y for i in res])

    for point in res:
        point.x += (l_min_x - min_x)
        point.y += (l_min_y - min_y)

    return res

def polygon_to_rect(polygon:list[Vector2]):
    x_list = [i.x for i in polygon]
    y_list = [i.y for i in polygon]
    min_x = min(x_list)
    max_x = max(x_list)
    min_y = min(y_list)
    max_y = max(y_list)
    the_rect = FRect(min_x, min_y, max_x - min_x, max_y - min_y)
    return the_rect