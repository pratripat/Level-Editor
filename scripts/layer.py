import pygame
from .chunk import Chunk

class Layer:
    def __init__(self, id, level_editor):
        self.id = id
        self.level_editor = level_editor
        self.chunks = {}

    def render(self):
        for chunk in self.visible_chunks:
            chunk.render(self.level_editor.screen, self.level_editor.workspace.scroll)
            pygame.draw.rect(self.level_editor.screen, (255,255,255), (chunk.position[0]-self.level_editor.workspace.scroll[0], chunk.position[1]-self.level_editor.workspace.scroll[1], self.level_editor.workspace.CHUNK_SIZE*self.level_editor.workspace.TILE_RES, self.level_editor.workspace.CHUNK_SIZE*self.level_editor.workspace.TILE_RES), 1)

    def update(self):
        for chunk in self.visible_chunks:
            chunk.update()

    def add_tile(self, tile):
        position = [self.level_editor.input_system.mouse_position[0]+self.level_editor.workspace.scroll[0], self.level_editor.input_system.mouse_position[1]+self.level_editor.workspace.scroll[1]]
        tile_position = [(position[0]//self.level_editor.workspace.TILE_RES)*self.level_editor.workspace.TILE_RES, (position[1]//self.level_editor.workspace.TILE_RES)*self.level_editor.workspace.TILE_RES]
        chunk = self.get_chunk(position)
        chunk.remove_tile(tile_position)
        chunk.add_tile(tile.image, tile_position, self.level_editor.workspace.CHUNK_SIZE*self.level_editor.workspace.current_tile_index)

    def get_chunk(self, position):
        position = ((position[0]//(self.level_editor.workspace.CHUNK_SIZE*self.level_editor.workspace.TILE_RES))*self.level_editor.workspace.CHUNK_SIZE*self.level_editor.workspace.TILE_RES, (position[1]//(self.level_editor.workspace.CHUNK_SIZE*self.level_editor.workspace.TILE_RES))*self.level_editor.workspace.CHUNK_SIZE*self.level_editor.workspace.TILE_RES)
        if position in self.chunks:
            return self.chunks[position]
        else:
            chunk = Chunk(position, self.level_editor.workspace.CHUNK_SIZE*self.level_editor.workspace.TILE_RES)
            self.chunks[position] = chunk
            return chunk

    @property
    def visible_chunks(self):
        visible_chunks = []
        for chunk in self.chunks.values():
            if self.level_editor.workspace.visible_rect.colliderect(chunk.rect):
                visible_chunks.append(chunk)
        return visible_chunks
