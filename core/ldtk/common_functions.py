from core.common_names import *

def find_level(world:dict,name:str):
    for level in world['levels']:
        if level['identifier'] == name:
            return level

def find_layer_instance(level:dict,name:str):
    for layer in level['layerInstances']:
        if layer['__identifier'] == name:
            return layer

def find_entity(entities:dict,name:str):
    for entity in entities['entityInstances']:
        if entity['__identifier'] == name:
            return entity

def find_in(list_:list,identifier:str):
    for item in list_:
        if item['__identifier'] == identifier:
            return item