from core.common_names import *
from core.ldtk.common_functions import *
import core.common_resources as cr
from core.ldtk.tileset import Tileset

class Level:
    def __init__(self):
        test_level = find_layer_instance(find_level(cr.world, 'Level_0'), 'Tiles_grid')
        self.grid_size = test_level['__gridSize']
        tileset_path = cr.levels_root + test_level['__tilesetRelPath']

        self.tileset = Tileset(tileset_path, self.grid_size)
        self.tiles = test_level['autoLayerTiles']


    def check_events( self ):
        ...

    def render( self ):
        for tile in self.tiles:
            surface = self.tileset.tiles[tile['t']]
            cr.screen.blit(surface,tile['px'])