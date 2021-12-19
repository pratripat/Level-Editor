class Chunk:
    def __init__(self, position):
        self.position = position
        self.entities = []

    def render(self, screen, scroll=[0,0]):
        for entity in self.entities:
            entity.render(screen, scroll)

    def update(self):
        for entity in self.entities:
            entity.update()
