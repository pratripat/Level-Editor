import time, random, json, pygame
from .funcs import load_images_from_spritesheet

class Tile:
    def __init__(self, chunk, image, position, filepath, spritesheet_index, image_scale, id=None):
        if id == None:
            self.id = int(time.time()*1000)
        else:
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

    def autotile(self, filepath, tiles, res, eight_bit_autotiling=False):
        if self.spritesheet_index == None:
            return

        #Gets neighbor with given tiles and direction
        def get_neighbor(tiles, direction):
            position = [self.position[0] + direction[0]*res, self.position[1] + direction[1]*res]
            for tile in tiles:
                if tile.position == position:
                    return '1'
            return '0'

        #Calculated the index of spritesheet using the config and binary
        def get_tile_index(key, binary, config):
            if binary in config.keys():
                return random.choice(config[binary])

            key_duplicate = key

            for i, number in enumerate(key):
                if number == '2':
                    key_duplicate = key_duplicate[:i] + binary[i] + key_duplicate[i+1:]

            if key_duplicate == binary:
                return random.choice(config[key])

            return None

        config = json.load(open(filepath, 'r'))

        #Directions (in particular order)
        directions = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        if eight_bit_autotiling:
            directions = [[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]]

        #Calculating the binary
        binary = ''
        for direction in directions:
            binary += get_neighbor(tiles, direction)

        #Getting the index
        index = None
        for key in config.keys():
            index = get_tile_index(key, binary, config)
            if index != None: break

        #Trying to change the image with the calculated index and spritesheet
        try:
            self.spritesheet_index = index
            image = load_images_from_spritesheet(self.filepath)[index]
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
