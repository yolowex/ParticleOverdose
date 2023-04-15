from core.common_names import *
from core.ldtk.common_functions import *
import core.common_resources as cr
from core.constants import *
from core.ldtk.tileset import Tileset


class Level :

    def __init__( self, scale: float = 2 ) :
        test_entities = find_layer_instance(find_level(cr.world, 'Level_0'), 'Entities')
        test_level = find_layer_instance(find_level(cr.world, 'Level_0'), 'Tiles_grid')
        collidables = find_layer_instance(find_level(cr.world, 'Level_0'), 'Collidables')
        collision_boxs = find_layer_instance(find_level(cr.world, 'Level_0'), 'CollisionBoxs')
        water_boxs = find_layer_instance(find_level(cr.world, 'Level_0'), 'WaterBoxs')
        lava_boxs = find_layer_instance(find_level(cr.world, 'Level_0'), 'LavaBoxs')
        upgradables = find_layer_instance(find_level(cr.world, 'Level_0'), 'Upgradables')


        self.lowest_tile = None

        self.total_diamonds = 0
        self.grid_size = test_level['__gridSize']
        tileset_path = cr.levels_root + test_level['__tilesetRelPath']

        self.player = find_entity(test_entities, 'Player')
        self.player_pos = [self.player['px'][0] * scale, self.player['px'][1] * scale]
        self.player_size = self.player['width'] * scale * 0.8, self.player['height'] * scale * 0.8

        self.collision_box_map = {}

        self.tileset = Tileset(tileset_path, self.grid_size, scale)
        self.tiles = test_level['autoLayerTiles']

        for tile in self.tiles :
            tile['px'][0] *= scale
            tile['px'][1] *= scale

        for sprite in self.tileset.tiles :
            sprite.transform_by_rel(scale, scale)

        self._inner_box_list = []
        self._water_box_list = []
        self._lava_box_list = []

        for entity in collidables['entityInstances'] :
            if entity['__identifier'] != 'Collidable' :
                continue
            rect = FRect(entity['px'][0] * scale, entity['px'][1] * scale, entity['width'] * scale,
                entity['height'] * scale)

            if self.lowest_tile is None:
                self.lowest_tile = rect.y + rect.h

            if rect.y + rect.h > self.lowest_tile:
                self.lowest_tile = rect.y + rect.h


            self._inner_box_list.append(rect)

        for entity in collision_boxs['entityInstances'] :
            if entity['__identifier'] != 'CollisionBox' :
                continue
            rect = FRect(entity['px'][0] * scale, entity['px'][1] * scale, entity['width'] * scale,
                entity['height'] * scale)

            self.collision_box_map[len(self.collision_box_map)] = {"rect" : rect,
                "collidables" : [], "tiles" : [],"water_boxs":[],"lava_boxs":[]}


        for entity in water_boxs['entityInstances'] :
            if entity['__identifier'] != 'WaterBox' :
                continue
            rect = FRect(entity['px'][0] * scale, entity['px'][1] * scale, entity['width'] * scale,
                entity['height'] * scale)

            self._water_box_list.append(rect)

        for entity in lava_boxs['entityInstances'] :
            if entity['__identifier'] != 'LavaBox' :
                continue
            rect = FRect(entity['px'][0] * scale, entity['px'][1] * scale, entity['width'] * scale,
                entity['height'] * scale)

            self._lava_box_list.append(rect)

        self.diamonds = []
        self.sword_upgradables = {}

        for entity in upgradables['entityInstances'] :
            if entity['__identifier'] != 'Upgradable' :
                continue

            name = find_in(entity['fieldInstances'],'String')['__value']

            if name is None:
                continue

            rect = FRect(entity['px'][0] * scale, entity['px'][1] * scale, entity['width'] * scale,
                entity['height'] * scale)
            rect.x -= rect.w / 2
            rect.y -= rect.h / 2

            if name == "diamond":
                self.diamonds.append({"rect":rect, "is_taken":False, "angle":0})
            else:
                self.sword_upgradables[name] = {"rect":rect, "is_taken":False, "angle":0}

        self.total_diamonds = len(self.diamonds)

        for key in self.collision_box_map:
            box = self.collision_box_map[key]['rect']
            for tile,c in zip(self.tiles[::-1],range(len(self.tiles))[::-1]) :
                surface = self.tileset.tiles[tile['t']].transformed_surface
                px = list(tile['px'])
                size = surface.get_size()
                rect = FRect(px[0], px[1], size[0], size[1])

                if box.colliderect(rect) :
                    self.collision_box_map[key]['tiles'].append(tile)
                    self.tiles.pop(c)
                    continue

        for key in self.collision_box_map :
            box = self.collision_box_map[key]['rect']
            for inner_box, c in zip(self._inner_box_list[: :-1], range(len(self._inner_box_list))[: :-1]) :
                if box.colliderect(inner_box) :
                    self.collision_box_map[key]['collidables'].append(inner_box)
                    continue

        for key in self.collision_box_map :
            box = self.collision_box_map[key]['rect']
            for inner_box, c in zip(self._water_box_list[: :-1], range(len(self._water_box_list))[: :-1]) :
                if box.colliderect(inner_box) :
                    self.collision_box_map[key]['water_boxs'].append(inner_box)
                    continue

        for key in self.collision_box_map :
            box = self.collision_box_map[key]['rect']
            for inner_box, c in zip(self._lava_box_list[: :-1], range(len(self._lava_box_list))[: :-1]) :
                if box.colliderect(inner_box) :
                    self.collision_box_map[key]['lava_boxs'].append(inner_box)

                    continue







    def init( self ) :
        self.tileset.init()
        cr.diamond.transform_by_height(self.grid_size)

    def check_events( self ) :



        for name,values in self.sword_upgradables.items():
            values['angle'] += cr.event_holder.delta_time * 45

            if name in cr.game.player.locked_swords_list:
                if cr.game.player.rect.colliderect(values['rect']):
                    cr.game.player.locked_swords_list.remove(name)
                    values['is_taken'] = True


        for values in self.diamonds:
            if values['is_taken']:
                continue

            values['angle'] += cr.event_holder.delta_time * - 65

            if cr.game.player.rect.colliderect(values['rect']) :
                cr.game.player.acquired_diamonds += 1
                values['is_taken'] = True


    # Bad usage of words, box means collidable here
    @property
    def inner_box_list( self ):
        cp = cr.camera
        scr_rect = FRect(cr.screen.get_rect())
        scr_rect.x -= cp.x
        scr_rect.y -= cp.y

        inner_boxs = []

        for box in self.collision_box_map:
            rect = self.collision_box_map[box]['rect'].copy()
            if rect.colliderect(scr_rect):
                inner_boxs.extend(self.collision_box_map[box]['collidables'])

        return inner_boxs

    @property
    def water_colliders_list( self ):
        cp = cr.camera
        scr_rect = FRect(cr.screen.get_rect())
        scr_rect.x -= cp.x
        scr_rect.y -= cp.y

        water_colliders = []

        for box in self.collision_box_map :
            rect = self.collision_box_map[box]['rect'].copy()
            if rect.colliderect(scr_rect) :
                water_colliders.extend(self.collision_box_map[box]['water_boxs'])

        return water_colliders


    @property
    def lava_colliders_list( self ) :
        cp = cr.camera
        scr_rect = FRect(cr.screen.get_rect())
        scr_rect.x -= cp.x
        scr_rect.y -= cp.y

        lava_colliders = []

        for box in self.collision_box_map :
            rect = self.collision_box_map[box]['rect'].copy()
            if rect.colliderect(scr_rect) :
                lava_colliders.extend(self.collision_box_map[box]['lava_boxs'])

        return lava_colliders

    def render_upgradables( self ):
        for name,values in self.sword_upgradables.items():
            if name in cr.game.player.locked_swords_list or name == 'diamond':
                surface = cr.right_sword_dict[name].transformed_surface
                surface = pg.transform.rotate(surface,values['angle'])
                surface_rect = surface.get_rect()
                surface_rect.center = values['rect'].center
                surface_rect.x += cr.camera.x
                surface_rect.y += cr.camera.y
                rect = values['rect'].copy()
                rect.x += cr.camera.x
                rect.y += cr.camera.y


                pg.draw.rect(cr.screen,"gold",rect,width=5)

                cr.screen.blit(surface,surface_rect)

        for values in self.diamonds:
            if not values['is_taken']:
                surface = cr.diamond.transformed_surface
                surface = pg.transform.rotate(surface, values['angle'])
                surface_rect = surface.get_rect()
                surface_rect.center = values['rect'].center
                surface_rect.x += cr.camera.x
                surface_rect.y += cr.camera.y
                rect = values['rect'].copy()
                rect.x += cr.camera.x
                rect.y += cr.camera.y


                cr.screen.blit(surface, surface_rect)

    def render( self ) :
        cp = cr.camera.pos

        rendered_tiles = 0
        for box in self.collision_box_map :
            rect = self.collision_box_map[box]['rect'].copy()
            rect.x += cp.x
            rect.y += cp.y
            scr_rect = FRect(cr.screen.get_rect())
            if scr_rect.colliderect(rect) :
                for tile in self.collision_box_map[box]['tiles']:
                    surface = self.tileset.tiles[tile['t']].transformed_surface
                    px = list(tile['px'])
                    px = [cp.x + px[0], cp.y + px[1]]
                    cr.screen.blit(surface, px)
                    rendered_tiles += 1


        self.render_upgradables()
