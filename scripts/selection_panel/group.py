import pygame, os, json
from .image import Image
from ..funcs import *

RESOLUTION = 48

class Group:
    def __init__(self, path, name, editor):
        self.path = path
        self.name = name
        self.editor = editor
        self.images = []
        self.load()

    def load(self):
        y = 80
        for filename in os.listdir(self.path):
            x = 20

            data = json.load(open(self.path+'/'+filename, 'r'))

            id = data['id']
            filename = data['filename']
            autotile_config = data['autotile_config']
            indexes = data['indexes']
            resize = data['resize']
            scale = data['scale']

            images = load_images_from_spritesheet(filename)

            if len(images) == 0:
                images = [spritesheet]
                indexes = [0]

            for index in indexes:
                if index >= len(images):
                    print('continuing')
                    continue

                image = images[index]

                if resize:
                    if not scale:
                        scale = (RESOLUTION/image.get_width(), RESOLUTION/image.get_height())

                    image = pygame.transform.scale(image, (image.get_width()*scale, image.get_height()*scale))

                image_object = Image(self.editor, id, (x, y), image, autotile_config)

                self.images.append(image_object)

                y += image.get_width()+10

            if y > self.editor.screen.get_height():
                y = 40
                x += image.get_width()+10

    def render(self):
        for image in self.images:
            image.render()

    def render_name(self):
        self.editor.font.render(self.editor.screen, self.name, (150, 30), center=(True, True), scale=2, color=(13,19,42))
