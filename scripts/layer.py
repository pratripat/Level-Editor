from .chunk import Chunk

class Layer:
    def __init__(self, id, level_editor):
        self.id = id
        self.level_editor = level_editor
        self.chunks = {}

    def render(self):
        for chunk in self.visible_chunks:
            chunk.render(self.level_editor.screen, self.level_editor.workspace.scroll)

    def update(self):
        for chunk in self.visible_chunks:
            chunk.update()

    def add_tile(self, tile):
        position = [self.level_editor.input_system.mouse_position[0]+self.level_editor.workspace.scroll[0], self.level_editor.input_system.mouse_position[1]+self.level_editor.workspace.scroll[1]]
        tile_position = [(position[0]//self.level_editor.workspace.TILE_SIZE)*self.level_editor.workspace.TILE_SIZE, (position[1]//self.level_editor.workspace.TILE_SIZE)*self.level_editor.workspace.TILE_SIZE]
        chunk = self.get_chunk(position)
        chunk.remove_tile(tile_position)
        chunk.add_tile(tile.image, tile_position, self.level_editor.workspace.current_tile_index)

    def get_chunk(self, position):
        position = ((position[0]//self.level_editor.workspace.CHUNK_SIZE)*self.level_editor.workspace.CHUNK_SIZE, (position[1]//self.level_editor.workspace.CHUNK_SIZE)*self.level_editor.workspace.CHUNK_SIZE)
        if position in self.chunks:
            return self.chunks[position]
        else:
            chunk = Chunk(position)
            self.chunks[position] = chunk
            return chunk

    @property
    def visible_chunks(self):
        visible_chunks = []
        for chunk_pos in self.chunks:
            if self.level_editor.workspace.visible_rect.collidepoint(chunk_pos):
                visible_chunks.append(self.chunks[chunk_pos])
        return visible_chunks
