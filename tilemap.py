import pygame, json, sys
from scripts.funcs import *

RES = 48

class Tilemap:
    def __init__(self, filename):
        self.filename = filename
        self.entities = []
        self.load()

    #Loads the json file
    def load(self):
        data = json.load(open(self.filename, 'r'))
        for position in data:
            pos, layer = position.split(':')
            id, filepath, index, scale = data[position]

            x, y = pos.split(';')
            pos = [int(x)*RES, int(y)*RES]

            dimensions = load_images_from_spritesheet('data/graphics/spritesheet/'+filepath+'.png')[index].get_size()
            dimensions = [dimensions[0]*scale, dimensions[1]*scale]

            offset = self.load_offset(id, index)

            self.entities.append({
                'position': pos,
                'offset': offset,
                'layer': layer,
                'id': id,
                'filepath': filepath,
                'index': index,
                'scale': scale,
                'dimensions': dimensions
            })

    #Loads offset with id and index
    def load_offset(self, id, index):
        try:
            offset_data = json.load(open(f'data/config/offsets/{id}.json', 'r'))
            offset = offset_data[str(index)]
            return offset
        except:
            return [0,0]

    #Returns entities that are colliding with the given rect
    def get_colliding_entities(self, ids, rect):
        entities = []
        colliding_rects = []

        for id in ids:
            entities.extend(self.get_tiles_with_id(id))

        for entity in entities:
            entity_rect = pygame.Rect(entity['position'][0]+entity['offset'][0], entity['position'][1]+entity['offset'][1], *entity['dimensions'])
            if entity_rect.colliderect(rect):
                colliding_rects.append(entity_rect)

        return colliding_rects

    #Returns entities with the same id and layer
    def get_tiles_with_id(self, id, layer=None):
        entities = []
        for entity in self.entities:
            if entity['id'] == id:
                if layer != None and entity['layer'] != layer:
                    continue
                entities.append(entity)
        return entities

    #Removes a entity from given position and layer
    def remove_entity(self, pos, layer=None):
        for entity in self.entities[:]:
            if entity['position'] == pos:
                if layer != None and entity['layer'] != layer:
                    continue
                self.entities.remove(entity)
