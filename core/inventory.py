from core.constants import *
from core.common_names import *
import core.common_resources as cr

class Inventory:
    def __init__( self ):
        rect = FRect(0,0,cr.screen.get_height()/7,cr.screen.get_height()/7)
        gap_unit = cr.screen.get_height()/7/6
        self.inactive_color = "gray"
        self.active_color = Color(155,30,12)

        rect_0 = rect.copy()
        rect_0.y+=rect.h*0 + gap_unit *0.5

        rect_1 = rect.copy()
        rect_1.y+=rect.h*1 + gap_unit *1.5
        rect_2 = rect.copy()
        rect_2.y+=rect.h*2 + gap_unit *2.5
        rect_3 = rect.copy()
        rect_3.y+=rect.h*3 + gap_unit *3.5
        rect_4 = rect.copy()
        rect_4.y+=rect.h*4 + gap_unit *4.5
        rect_5 = rect.copy()
        rect_5.y+=rect.h*5 + gap_unit *5.5




        self.items = {
            "blood":{"rect":rect_0,"text":"blood lust"},
            "evil":{"rect":rect_1,"text":"evergreen evil"},
            "hawk":{"rect":rect_2,"text":"blue hawk"},
            "light":{"rect":rect_3,"text":"the way of light"},
            "desire":{"rect":rect_4,"text":"burning desire"},
            "death":{"rect":rect_5,"text":"death wish"}
        }




    def check_events( self ):
        ...

    def render( self ):
        for key,value in self.items.items():
            rect = value['rect']
            color = self.active_color

            pg.draw.rect(cr.screen,color,rect,width = 5)