from core.common_names import *

def find_level(world:dict,name:str):
    for level in world['levels']:
        if level['identifier'] == name:
            return level

def find_layer_instance(level:dict,name:str):
    for level in level['layerInstances']:
        if level['__identifier'] == name:
            return level
