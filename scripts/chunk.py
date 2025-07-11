import pygame
from .funcs import load_images_from_spritesheet, load_images_from_tilemap
from .tile import Tile

class Chunk:
    def __init__(self, position, res):
        self.position = position
        self.size = [res, res]
        self.tiles = []

    def render(self, screen, scroll=[0,0]):
        for tile in self.tiles:
            tile.render(screen, scroll)

    def update(self):
        for tile in self.tiles:
            tile.update()

    def load_tile(self, position, id, filepath, spritesheet_index, image_scale):
        if spritesheet_index != None:
            try:
                image = load_images_from_spritesheet(filepath)[spritesheet_index]
            except:
                image = load_images_from_tilemap(filepath)[spritesheet_index]
        else:
            image = pygame.image.load(filepath).convert()

        self.add_tile(image, position, filepath, spritesheet_index, image_scale, id)

    def add_tile(self, image, position, filepath, spritesheet_index, image_scale, id=None):
        image = pygame.transform.scale(image, (int(image.get_width()*image_scale), int(image.get_height()*image_scale)))
        image.set_colorkey((0,0,0))

        if id == None:
            id = self.get_unique_id()

        tile = Tile(self, image, position, filepath, spritesheet_index, image_scale, id)
        self.tiles.append(tile)
        return tile

    def remove_tile(self, position):
        tiles = [tile for tile in self.tiles if tile.position == position]
        for tile in tiles:
            self.tiles.remove(tile)
        return tiles

    def get_tile(self, position):
        for tile in self.tiles:
            if tile.position == position:
                return tile

    def get_unique_id(self):
        if len(self.tiles) == 0:
            return 10000
        return max([tile.id for tile in self.tiles])+1

    @property
    def rect(self):
        return pygame.Rect(*self.position, *self.size)
