import time, random, json, pygame
from .funcs import load_images_from_spritesheet, load_images_from_tilemap

class Tile:
    def __init__(self, chunk, image, position, filepath, spritesheet_index, image_scale, id):
        self.id = id
        self.chunk = chunk
        self.image = image
        self.position = position
        self.filepath = filepath
        self.spritesheet_index = spritesheet_index
        self.image_scale = image_scale

    def render(self, screen, scroll=[0,0]):
        screen.blit(self.image, (self.position[0]-scroll[0], self.position[1]-scroll[1]))

    def update(self):
        pass

    def autotile(self, filepath, tiles, res):
        if self.spritesheet_index == None:
            return

        #Gets neighbor with given tiles and direction
        def get_neighbor(tiles, direction):
            position = [self.position[0] + direction[0]*res, self.position[1] + direction[1]*res]
            for tile in tiles:
                if tile.position == position:
                    return '1'
            return '0'

        def get_tile_index(config, binary):
            if binary in config:
                return random.choice(config[binary])

            # Fallback: partial match (strict on cross directions)
            fallback = []
            for key in config:
                # Check cardinal (even index)
                if all(binary[i] == key[i] for i in range(0, 8, 2)):
                    fallback.append(key)

            # Check diagonal consistency (odd index)
            fallback = [key for key in fallback if all(
                key[i] == '0' or binary[i] == '1' for i in range(1, 8, 2)
            )]

            if fallback:
                return random.choice(config[fallback[0]])

            return None

        config = json.load(open(filepath, 'r'))

        #Directions (in particular order)
        directions = [[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]]

        #Calculating the binary
        binary = ''
        for direction in directions:
            binary += get_neighbor(tiles, direction)

        #Getting the index
        index = get_tile_index(config, binary)

        #Trying to change the image with the calculated index and spritesheet
        try:
            try: 
                image = load_images_from_spritesheet(self.filepath)[index]
            except: 
                image = load_images_from_tilemap(self.filepath)[index]

            self.spritesheet_index = index
            image = pygame.transform.scale(image, (int(image.get_width() * self.image_scale), int(image.get_height() * self.image_scale)))
            image.set_colorkey((0,0,0))
            self.image = image

        except Exception as e:
            print('AUTOTILE ERROR...')
            print(e)

    def get_data(self, tilemaps):
        return [
            self.position,
            self.id,
            tilemaps.index(self.filepath),
            self.spritesheet_index,
            self.image_scale
        ]
