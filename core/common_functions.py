from core.common_names import *
import numpy

def rect_convert_polygon( rect: FRect ) :
    return [Vector2(i) for i in
        [[rect.x, rect.y], [rect.x + rect.w, rect.y], [rect.x + rect.w, rect.y + rect.h],
            [rect.x , rect.y + rect.h],]]

def image_to_surface(image:Image) -> Surface:
    mode = image.mode
    size = image.size
    data = image.tobytes()

    surface = pg.image.fromstring(data, size, mode)
    return surface

def shift_points_to_origin(points:list[Vector2]):
    min_x = min([i.x for i in points])
    min_y = min([i.y for i in points])

    res_points = [i.copy() for i in points]
    for point in res_points:
        point.x -= min_x
        point.y -= min_y

    return res_points




def rotate_point(origin, point, angle):
    angle = math.radians(angle)
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return Vector2(qx, qy)


def percent(All,part):
    return (100/All) * part

def find_co_effs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)