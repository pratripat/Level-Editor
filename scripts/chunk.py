from .tile import Tile

class Chunk:
    def __init__(self, position):
        self.position = position
        self.tiles = []

    def render(self, screen, scroll=[0,0]):
        for entity in self.tiles:
            entity.render(screen, scroll)

    def update(self):
        for entity in self.tiles:
            entity.update()

    def add_tile(self, image, position, index):
        tile = Tile(self, image, position, index)
        self.tiles.append(tile)

    def remove_tile(self, position):
        tiles = [tile for tile in self.tiles if tile.position == position]
        for tile in tiles:
            self.tiles.remove(tile)

    def get_tile(self, position):
        for tile in self.tiles:
            if tile.position == position:
                return tile
