from core.common_names import *

class Camera:
    def __init__(self,pos:Vector2):
        self.pos = pos

    @property
    def x(self):
        return self.pos.x

    @property
    def y( self ):
        return self.pos.y
