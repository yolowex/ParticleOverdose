import pygame_gui.core.utility

from core.common_names import *

class Tileset:
    def __init__(self,path:str,grid_size:float):
        self.path = path
        self.surface = pg.image.load(self.path)
        self.grid_size = grid_size
        self.tiles = []
        self.create_tiles()

    def create_tiles( self ):
        w = h = self.grid_size
        rect = FRect(0,0,w,h)

        w_index = 0
        h_index = 0
        base_tile = Surface((w,h))

        while True:
            rect.x = w_index
            rect.y = h_index
            tile = base_tile.copy()
            tile.blit(self.surface,[0,0],rect)
            self.tiles.append(tile)

            w_index += 1
            if not self.surface.get_rect().contains(rect):
                w_index = 0
                h_index += 1

            if rect.y > self.surface.get_rect().h:
                break


