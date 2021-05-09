import pygame, json, sys
from scripts.funcs import *

RES = 48

class Tilemap:
    def __init__(self, filename):
        self.filename = filename
        self.entities = []
        self.load()

    def load(self):
        data = json.load(open(self.filename, 'r'))
        for position in data:
            pos, layer = position.split(':')
            id, filepath, index, scale = data[position]
            self.entities.append({
                'position': pos,
                'layer': layer,
                'id': id,
                'filepath': filepath,
                'index': index,
                'scale': scale
            })

    def render_entities(self, surface, scroll):
        for entity in self.entities:
            image = load_images_from_spritesheet(f'data/graphics/spritesheet/{entity["filepath"]}.png')[entity['index']]
            image = pygame.transform.scale(image, (image.get_width()*entity['scale'], image.get_height()*entity['scale']))

            x, y = entity['position'].split(';')
            position = [(int(float(x))*RES)-int(scroll[0]), (int(float(y))*RES)-int(scroll[1])]
            surface.blit(image, position)

if __name__ == '__main__':
    screen = pygame.display.set_mode((1000, 700), pygame.RESIZABLE)
    scroll = [0,0]

    tilemap = Tilemap('data/saved.json')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill((0,0,0))
        tilemap.render_entities(screen, scroll)
        pygame.display.update()
