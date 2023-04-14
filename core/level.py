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
        self.player_size = self.player['width']*scale *0.8, self.player['height']*scale *0.8

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

    def init( self ):
        self.tileset.init()

    def check_events( self ) :
        ...


    def render( self ) :
        cp = cr.camera.pos




        rendered_tiles = 0
        for tile in self.tiles :

            surface = self.tileset.tiles[tile['t']].transformed_surface
            px = list(tile['px'])
            px = [cp.x + px[0], cp.y + px[1]]
            size = surface.get_size()
            rect = FRect(px[0],px[1],size[0],size[1])

            scr_rect = FRect(cr.screen.get_rect())
            scr_rect.x -= scr_rect.w
            scr_rect.y -= scr_rect.h
            scr_rect.w += scr_rect.w
            scr_rect.h += scr_rect.h

            if scr_rect.colliderect(rect) :
                cr.screen.blit(surface, px)
                rendered_tiles +=1

        # t = 0
        #
        # for rect in cr.game.inner_box_list :
        #     rect = list(rect)
        #     o_rect = rect.copy()
        #
        #     rect[0] += cp.x
        #     rect[1] += cp.y
        #
        #     scr_rect = FRect(cr.screen.get_rect())
        #     scr_rect.x -= cp.x
        #     scr_rect.y -= cp.y
        #
        #     if scr_rect.colliderect(o_rect):
        #         pg.draw.rect(cr.screen, WHITE.lerp('red', 0.2), rect)
        #         pg.draw.rect(cr.screen, WHITE.lerp(BLACK, 0.5), rect, width=3)
        #         t+=1
        #
        # print(len(cr.game.inner_box_list),t)