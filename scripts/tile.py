import time

class Tile:
    def __init__(self, chunk, image, layer_index, position, filepath, spritesheet_index):
        self.id = time.time()
        self.chunk = chunk
        self.layer_index = layer_index
        self.image = image
        self.position = position
        self.filepath = filepath
        self.spritesheet_index = spritesheet_index

    def render(self, screen, scroll=[0,0]):
        screen.blit(self.image, (self.position[0]-scroll[0], self.position[1]-scroll[1]))

    def update(self):
        pass

    def get_data(self):
        return [
            self.position,
            self.id,
            self.filepath,
            self.spritesheet_index
        ]
