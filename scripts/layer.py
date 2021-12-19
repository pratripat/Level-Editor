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

    @property
    def visible_chunks(self):
        visible_chunks = []
        for chunk_pos in self.chunks:
            if self.level_editor.workspace.visible_rect.collidepoint(chunk_pos):
                visible_chunks.append(self.chunks[chunk_pos])
        return visible_chunks
