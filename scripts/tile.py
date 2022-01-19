import time, random, json, pygame
from .funcs import load_images_from_spritesheet

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
            if binary in config.keys():
                return random.choice(config[binary])

            #Checking the top right bottom left tiles
            keys = []
            for key in config.keys():
                for i, number in enumerate(binary):
                    if i % 2 == 0:
                        if number != key[i]:
                            break
                else:
                    keys.append(key)

            #Checking the diagonal tiles
            for key in keys[:]:
                for i, number in enumerate(key):
                    if i % 2 != 0:
                        if number == '1':
                            if binary[i] != '1':
                                keys.remove(key)
                                break

            #Returning the indexes with the calculated key
            if len(keys):
                key = keys[0]
                return random.choice(config[key])

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
