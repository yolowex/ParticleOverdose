from core.common_names import *
from core.common_functions import *
import core.common_resources as cr

class Sprite :

    def __init__( self, path: str ) :
        self.transform_point_dict = {}
        self.raw_surface = pg.image.load(path)
        self.raw_pil_image = Image.open(path)
        self.transformed_pil_image = self.raw_pil_image.copy()
        self.transformed_surface = self.raw_surface.copy()


    def get_diff( self ) :
        a = self.raw_surface.get_size()
        b = self.transformed_surface.get_size()

        return [b[0] / a[0], b[1] / a[1]]


    def transform( self, new_w, new_h ) :
        self.transformed_surface = pg.transform.scale(self.raw_surface, (new_w, new_h))


    def transform_by_height( self, new_h ) :
        current_h = self.raw_surface.get_height()
        new_w = self.raw_surface.get_width() * (new_h / current_h)

        self.transformed_surface = pg.transform.scale(self.raw_surface, (new_w, new_h))


    def transform_by_rel( self, rel_x, rel_y ) :
        new_w, new_h = self.raw_surface.get_size()
        new_w *= rel_x
        new_h *= rel_y

        self.transformed_surface = pg.transform.scale(self.raw_surface, (new_w, new_h))


    def transform_by_points( self, points,points_rect:FRect ) :
        points = [Vector2(int(i.x),int(i.y)) for i in points]
        points = shift_points_to_origin(points)
        points_rect = Rect(points_rect)
        key = "".join(str(i.x)+"-"+(str(i.y))+"-" for i in points)
        print(int(cr.event_holder.final_fps),len(self.transform_point_dict))
        if key in self.transform_point_dict:
            self.transformed_surface = self.transform_point_dict[key]

        else:
            co_effs = find_co_effs(rect_convert_polygon(FRect(self.raw_surface.get_rect())),
                                points)

            width, height = int(points_rect.w),int(points_rect.h)
            self.transformed_surface= self.raw_pil_image.transform((width, height), Image.PERSPECTIVE, co_effs,
                Image.NEAREST)

            self.transformed_surface = image_to_surface(self.transformed_surface).convert()
            self.transformed_surface.set_colorkey("black")
            self.transform_point_dict[key] = self.transformed_surface
