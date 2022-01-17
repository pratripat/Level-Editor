import pygame
from .chunk import Chunk
from .tile import Tile

class Layer:
    def __init__(self, id, level_editor):
        self.id = id
        self.level_editor = level_editor
        self.chunks = {}
        self.changes = []
        self.undos = []

    def render(self):
        for chunk in self.visible_chunks:
            chunk.render(self.level_editor.screen, self.level_editor.workspace.scroll)
            pygame.draw.rect(self.level_editor.screen, (255,255,255), (chunk.position[0]-self.level_editor.workspace.scroll[0], chunk.position[1]-self.level_editor.workspace.scroll[1], self.level_editor.workspace.CHUNK_SIZE*self.level_editor.workspace.TILE_RES, self.level_editor.workspace.CHUNK_SIZE*self.level_editor.workspace.TILE_RES), 1)

    def update(self):
        if len(self.changes) == 0:
            self.changes.append([tile for chunk in self.chunks.values() for tile in chunk.tiles])

        for chunk in self.visible_chunks:
            chunk.update()

        if self.level_editor.input_system.mouse_states['left'] and not any([menu.is_mouse_hovering() for menu in self.level_editor.menu_manager.menus]):
            self.add_change()

    def fill(self, position, depth=950):
        if depth == 0:
            return

        position = [(position[0]//self.level_editor.workspace.TILE_RES)*self.level_editor.workspace.TILE_RES, (position[1]//self.level_editor.workspace.TILE_RES)*self.level_editor.workspace.TILE_RES]
        for dir in [(0,-1), (1,0), (0,1), (-1,0)]:
            new_position = [position[0]+self.level_editor.workspace.TILE_RES*dir[0], position[1]+self.level_editor.workspace.TILE_RES*dir[1]]
            chunk = self.get_chunk(new_position)

            if chunk in self.visible_chunks:
                neighbor = chunk.get_tile(new_position)

                #If the neighbor is not yet defined, the neighbor becomes a tile object and is put into the tiles list
                if not neighbor:
                    tile, filepath, spritesheet_index, image_scale = self.level_editor.workspace.current_tile_data
                    chunk.add_tile(tile.image, new_position, filepath, spritesheet_index, image_scale)

                    self.fill(new_position, depth-1)

        if depth == 950:
            self.add_change()

    def autotile(self, autotile_tiles):
        chunks = []
        for tile in autotile_tiles:
            if tile.chunk not in chunks:
                chunks.append(tile.chunk)

        tiles = [tile for chunk in chunks for tile in chunk.tiles]

        for tile in autotile_tiles:
            if self.level_editor.tilemaps_manager.tilemaps[tile.filepath]:
                tile.autotile(self.level_editor.workspace.autotile_filename, tiles, self.level_editor.workspace.TILE_RES, True)

        self.add_change()

    def undo(self):
        if len(self.changes) == 0:
            return

        self.undos.append([Tile(tile.chunk, tile.image, tile.position, tile.filepath, tile.spritesheet_index, tile.image_scale, tile.id) for chunk in self.chunks.values() for tile in chunk.tiles])
        self.undos[-200:]

        for chunk in self.chunks.values():
            chunk.tiles.clear()

        latest_change = self.changes.pop()
        for tile in latest_change:
            chunk = tile.chunk
            chunk.tiles.append(tile)

        for position in list(self.chunks.keys())[:]:
            if len(self.chunks[position].tiles) == 0:
                del self.chunks[position]

    def redo(self):
        if len(self.undos) == 0:
            return

        self.changes.append([Tile(tile.chunk, tile.image, tile.position, tile.filepath, tile.spritesheet_index, tile.image_scale, tile.id) for chunk in self.chunks.values() for tile in chunk.tiles])
        self.changes[-200:]

        for chunk in self.chunks.values():
            chunk.tiles.clear()

        latest_undo = self.undos.pop()
        for tile in latest_undo:
            chunk = tile.chunk
            chunk.tiles.append(tile)

        for position in list(self.chunks.keys())[:]:
            if len(self.chunks[position].tiles) == 0:
                del self.chunks[position]

    def get_tile_with_position(self, position):
        chunk = self.get_chunk(position)
        if chunk:
            return chunk.get_tile(position)

    def get_tile_neighbors(self, tile):
        neighbors = []
        position = [(tile.position[0]//self.level_editor.workspace.TILE_RES)*self.level_editor.workspace.TILE_RES, (tile.position[1]//self.level_editor.workspace.TILE_RES)*self.level_editor.workspace.TILE_RES]
        for dir in [(0,-1), (1,0), (0,1), (-1,0)]:
            new_position = [position[0]+self.level_editor.workspace.TILE_RES*dir[0], position[1]+self.level_editor.workspace.TILE_RES*dir[1]]
            chunk = self.get_chunk(new_position)

            if chunk in self.visible_chunks:
                neighbor = chunk.get_tile(new_position)

                if neighbor:
                    neighbors.append(neighbor)
        return neighbors

    def add_tile(self, tile, filepath, spritesheet_index, image_scale):
        position = [self.level_editor.input_system.mouse_position[0]+self.level_editor.workspace.scroll[0], self.level_editor.input_system.mouse_position[1]+self.level_editor.workspace.scroll[1]]
        tile_position = [(position[0]//self.level_editor.workspace.TILE_RES)*self.level_editor.workspace.TILE_RES, (position[1]//self.level_editor.workspace.TILE_RES)*self.level_editor.workspace.TILE_RES]
        chunk = self.get_chunk(position)
        chunk.remove_tile(tile_position)
        tile = chunk.add_tile(tile.image, tile_position, filepath, spritesheet_index, image_scale)
        return tile

    def remove_tile(self, position):
        tile_position = [(position[0]//self.level_editor.workspace.TILE_RES)*self.level_editor.workspace.TILE_RES, (position[1]//self.level_editor.workspace.TILE_RES)*self.level_editor.workspace.TILE_RES]
        chunk = self.get_chunk(tile_position)
        chunk.remove_tile(tile_position)

    def remove_tiles(self, tiles):
        self.add_change()
        for tile in tiles:
            chunk = tile.chunk
            chunk.tiles.remove(tile)

    def load(self, data, tilemaps):
        for tile_data in data:
            position, id, filepath_index, spritesheet_index, image_scale = tile_data
            filepath = tilemaps[filepath_index]
            chunk = self.get_chunk(position)
            chunk.load_tile(position, id, filepath, spritesheet_index, image_scale)
            self.changes.clear()

    def add_change(self):
        self.changes.append([Tile(chunk, tile.image, tile.position, tile.filepath, tile.spritesheet_index, tile.image_scale, tile.id) for chunk in self.chunks.values() for tile in chunk.tiles])
        self.changes[-200:]
        self.undos.clear()

    def get_chunk(self, position):
        position = ((position[0]//(self.level_editor.workspace.CHUNK_SIZE*self.level_editor.workspace.TILE_RES))*self.level_editor.workspace.CHUNK_SIZE*self.level_editor.workspace.TILE_RES, (position[1]//(self.level_editor.workspace.CHUNK_SIZE*self.level_editor.workspace.TILE_RES))*self.level_editor.workspace.CHUNK_SIZE*self.level_editor.workspace.TILE_RES)
        if position in self.chunks:
            return self.chunks[position]
        else:
            chunk = Chunk(position, self.level_editor.workspace.CHUNK_SIZE*self.level_editor.workspace.TILE_RES)
            self.chunks[position] = chunk
            return chunk

    def get_tiles_within_rect(self, rect):
        chunks = [chunk for chunk in self.chunks.values() if chunk.rect.colliderect(rect)]
        tiles = []

        for tile in [tile for chunk in chunks for tile in chunk.tiles]:
            if tile not in tiles:
                if tile.position[0] > rect[0] and tile.position[1] > rect[1] and tile.position[0]+self.level_editor.workspace.TILE_RES < rect[0]+rect[2] and tile.position[1]+self.level_editor.workspace.TILE_RES < rect[1]+rect[3]:
                    tiles.append(tile)

        return tiles

    def get_data(self, tilemaps):
        return [
            self.id,
            [tile.get_data(tilemaps) for chunk in self.chunks.values() for tile in chunk.tiles]
        ]

    @property
    def visible_chunks(self):
        visible_chunks = []
        for chunk in self.chunks.values():
            if self.level_editor.workspace.visible_rect.colliderect(chunk.rect):
                visible_chunks.append(chunk)
        return visible_chunks

    @property
    def index(self):
        return int(self.id.split('_')[1])
