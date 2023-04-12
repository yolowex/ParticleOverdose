from core.common_names import *
from core.ldtk.common_functions import *
import core.common_resources as cr
from core.constants import *
from core.ldtk.tileset import Tileset


class Level :

    def __init__( self,scale:float=2 ) :
        test_entities = find_layer_instance(find_level(cr.world, 'Level_0'), 'Entities')
        test_level = find_layer_instance(find_level(cr.world, 'Level_0'), 'Tiles_grid')
        collision_boxs = find_layer_instance(find_level(cr.world, 'Level_0'), 'CollisionBoxs')

        self.grid_size = test_level['__gridSize']
        tileset_path = cr.levels_root + test_level['__tilesetRelPath']

        self.player = find_entity(test_entities, 'Player')
        self.player_pos = [self.player['px'][0]*scale,self.player['px'][1]*scale]
        self.player_size = self.player['width']*scale, self.player['height']*scale

        self.tileset = Tileset(tileset_path, self.grid_size, scale)
        self.tiles = test_level['autoLayerTiles']

        for tile in self.tiles:
            tile['px'][0]*=scale
            tile['px'][1]*=scale


        for sprite in self.tileset.tiles :

            sprite.transform_by_rel(scale, scale)

        self.inner_box_list = []
        for entity in collision_boxs['entityInstances'] :
            if entity['__identifier'] != 'CollisionBox' :
                continue
            rect = FRect(entity['px'][0] * scale, entity['px'][1] * scale, entity['width'] * scale,
                entity['height'] * scale)

            self.inner_box_list.append(rect)



    def check_events( self ) :
        ...


    def render( self ) :
        cp = cr.camera.pos
        for rect in self.inner_box_list :
            rect = list(rect)
            rect[0] += cp.x
            rect[1] += cp.y

            pg.draw.rect(cr.screen, WHITE.lerp('red', 0.2), rect)
            pg.draw.rect(cr.screen, WHITE.lerp(BLACK, 0.5), rect, width=3)

        for tile in self.tiles :
            surface = self.tileset.tiles[tile['t']].transformed_surface
            px = tile['px']
            cr.screen.blit(surface, [cp.x + px[0], cp.y + px[1]])
