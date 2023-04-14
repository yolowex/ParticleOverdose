from core.common_names import *
from core.sprite import Sprite

class Tileset:
    def __init__(self,path:str,grid_size:float,scale:float=1):
        self.path = path
        self.surface = pg.image.load(self.path)
        # self.surface.set_colorkey("black")
        self.grid_size = grid_size
        self.tiles:list[Sprite] = []
        self.scale = scale
        self.create_tiles()

    def init( self ):
        for tile in self.tiles:
            tile.transformed_surface.set_colorkey("black")

    def create_tiles( self ):
        w = h = self.grid_size
        rect = FRect(0,0,w,h)

        w_index = 0
        h_index = 0
        base_tile = Surface((w,h))
        counter = 0

        while True:
            rect.x = w_index * w
            rect.y = h_index * h
            tile = base_tile.copy()
            tile.blit(self.surface,[0,0],rect)
            sprite = Sprite(surface=tile)

            if not rect.x >= self.surface.get_rect().w:
                self.tiles.append(sprite)
                counter += 1

            w_index += 1
            if not self.surface.get_rect().contains(rect):
                w_index = 0
                h_index += 1

            if rect.y > self.surface.get_rect().h:
                break


