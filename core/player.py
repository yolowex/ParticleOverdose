from core.common_names import *
import core.common_resources as cr
from core.constants import *

class Player:
    def __init__(self,rect:FRect):
        self.rect = rect
        self.color = WHITE
        self.border_color = BLACK.lerp(WHITE,0.5)
        self.border_size = int(self.rect.w * 0.1)
        if self.border_size < 1:
            self.border_size = 1

    def check_events( self ):
        ...

    def render( self ):
        pg.draw.rect(cr.screen,self.color,self.rect)
        pg.draw.rect(cr.screen,self.border_color,self.rect,width=self.border_size)

