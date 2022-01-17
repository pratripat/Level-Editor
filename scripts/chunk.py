import pygame
from .funcs import load_images_from_spritesheet
from .tile import Tile

class Chunk:
    def __init__(self, position, res):
        self.position = position
        self.size = [res, res]
        self.tiles = []

    def render(self, screen, scroll=[0,0]):
        for entity in self.tiles:
            entity.render(screen, scroll)

    def update(self):
        for entity in self.tiles:
            entity.update()

    def load_tile(self, position, id, filepath, spritesheet_index, image_scale):
        if spritesheet_index != None:
            image = load_images_from_spritesheet(filepath)[spritesheet_index]
        else:
            image = pygame.image.load(filepath)

        self.add_tile(image, position, filepath, spritesheet_index, image_scale, id)

    def add_tile(self, image, position, filepath, spritesheet_index, image_scale, id=None):
        image = pygame.transform.scale(image, (int(image.get_width()*image_scale), int(image.get_height()*image_scale)))
        image.set_colorkey((0,0,0))
        tile = Tile(self, image, position, filepath, spritesheet_index, image_scale, id)
        self.tiles.append(tile)
        return tile

    def remove_tile(self, position):
        tiles = [tile for tile in self.tiles if tile.position == position]
        for tile in tiles:
            self.tiles.remove(tile)

    def get_tile(self, position):
        for tile in self.tiles:
            if tile.position == position:
                return tile

    @property
    def rect(self):
        return pygame.Rect(*self.position, *self.size)
