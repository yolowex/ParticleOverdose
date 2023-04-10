from core.common_names import *


def rect_convert_polygon( rect: FRect ) :
    return [Vector2(i) for i in
        [[rect.x, rect.y], [rect.x + rect.w, rect.y], [rect.x + rect.w, rect.y + rect.h],
            [rect.x , rect.y + rect.h],]]
