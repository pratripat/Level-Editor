class Tile:
    def __init__(self, chunk, image, position, tile_index, filepath, spritesheet_index):
        self.chunk = chunk
        self.image = image
        self.position = position
        self.tile_index = tile_index
        self.filepath = filepath
        self.spritesheet_index = spritesheet_index

    def render(self, screen, scroll=[0,0]):
        screen.blit(self.image, (self.position[0]-scroll[0], self.position[1]-scroll[1]))

    def update(self):
        pass    
