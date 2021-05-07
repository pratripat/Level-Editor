import pygame, os, json
from .image import Image
from ..funcs import *

class Group:
    def __init__(self, path, name, editor):
        self.path = path
        self.name = name
        self.editor = editor
        self.images = []
        self.current_image = None
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
            offset = data['offset']
            resize = data['resize']
            scale = data['scale']
            group_id = filename.split('.png')[0].split('/')[-1]

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
                        scale = (self.editor.res/image.get_width(), self.editor.res/image.get_height())

                    image = pygame.transform.scale(image, (image.get_width()*scale, image.get_height()*scale))

                image_object = Image(self.editor, index, id, self.name, group_id, (x, y), offset, image, autotile_config)

                self.images.append(image_object)

                y += image.get_width()+10

            if y > self.editor.screen.get_height():
                y = 40
                x += image.get_width()+10

    def render(self):
        if self.current_image:
            pygame.draw.rect(self.editor.screen, (255,255,0), (self.current_image.position[0]-2, self.current_image.position[1]-2, self.current_image.image.get_width()+4, self.current_image.image.get_height()+4))

        for image in self.images:
            image.render()

    def render_name(self):
        self.editor.font.render(self.editor.screen, '-'+self.name+'-', (150, 30), center=(True, True), color=(13,19,42))

    def update_on_mouse_click(self, position):
        for image in self.images:
            if image.clicked(position):
                self.current_image = image
                return
