
from core.constants import *
from core.common_names import *
import core.common_resources as cr


class Inventory :

    def __init__( self ) :
        rect = FRect(0, 0, cr.screen.get_height() / 7, cr.screen.get_height() / 7)
        gap_unit = cr.screen.get_height() / 7 / 6
        self.inactive_color = "gray"
        self.active_color = Color(155, 30, 12)

        rect_0 = rect.copy()
        rect_0.y += rect.h * 0 + gap_unit * 0.5

        rect_1 = rect.copy()
        rect_1.y += rect.h * 1 + gap_unit * 1.5
        rect_2 = rect.copy()
        rect_2.y += rect.h * 2 + gap_unit * 2.5
        rect_3 = rect.copy()
        rect_3.y += rect.h * 3 + gap_unit * 3.5
        rect_4 = rect.copy()
        rect_4.y += rect.h * 4 + gap_unit * 4.5
        rect_5 = rect.copy()
        rect_5.y += rect.h * 5 + gap_unit * 5.5

        self.selected_surface = Surface((rect.w,rect.h))
        self.selected_surface = self.selected_surface
        self.selected_surface.fill([180,150,150,125])

        self.items = {"evil" : {"rect" : rect_0, "text" : "blood lust"},
            "desire" : {"rect" : rect_1, "text" : "evergreen evil"},
            "light" : {"rect" : rect_2, "text" : "blue hawk"},
            "hawk" : {"rect" : rect_3, "text" : "the way of light"},
            "blood" : {"rect" : rect_4, "text" : "burning desire"},
            "death" : {"rect" : rect_5, "text" : "death wish"}}

        for key in self.items :
            item = self.items[key]
            item['sprite'] = Sprite(surface=cr.right_sword_dict[key].raw_surface)

            item['sprite'].transform_by_height(rect.h*0.8)
            item['locked_sprite'] = Sprite(surface=Surface((rect.w,rect.h)))

            gray_surface = pg.transform.grayscale(item['sprite'].transformed_surface)
            # gray_surface = item['sprite'].transformed_surface
            rect = item['locked_sprite'].raw_surface.get_rect()
            item['locked_sprite'].transform_by_height(rect.h)
            surface_rect = gray_surface.get_rect()
            surface_rect.center = rect.center


            item['locked_sprite'].transformed_surface.fill([0,0,0,150])
            item['locked_sprite'].transformed_surface.blit(gray_surface,surface_rect)





    def check_events( self ) :
        ...


    def render( self ) :
        for key, value in self.items.items() :
            rect = value['rect']
            color = self.inactive_color
            if cr.game.player.sword.name == key :
                color = self.active_color

            surface = value['sprite'].transformed_surface
            surface_rect = surface.get_rect()
            surface_rect.center = rect.center

            if not key in cr.game.player.locked_swords_list:
                cr.screen.blit(self.selected_surface,rect)
                cr.screen.blit(surface,surface_rect)
            else:
                cr.screen.blit(value['locked_sprite'].transformed_surface,rect)

            pg.draw.rect(cr.screen, color, rect, width=5)

