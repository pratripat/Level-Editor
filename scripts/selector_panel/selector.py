from settings import *
from .image import Image
from funcs import load_images_from_spritesheet

class Selector:
    def __init__(self, position, filename, id, autotile_config_path, resize, scale):
        self.position = position
        self.filename = filename
        self.id = id
        self.autotile_config_path = autotile_config_path
        self.resize = resize
        self.scale = scale

        self.images = []
        self.selected_image = None
        self.font = pygame.font.SysFont('comicsans', 30)
        self.label = self.font.render(self.id.capitalize(), 1, colors['white'])

        self.load_images()

    def show_label(self):
        #Renders the name of the selector
        screen.blit(self.label, self.position)

    def show(self):
        #Renders the images
        for image in self.images:
            image.show()

        #Renders border over the current selected image
        if self.selected_image:
            pygame.draw.rect(screen, colors['yellow'], (self.selected_image.position[0], self.selected_image.position[1], self.selected_image.get_width(), self.selected_image.get_height()), 2)

    def run(self, position, clicked):
        if clicked:
            for image in self.images:
                if image.is_clicked(position):
                    #Sets the current image to the image the mouse is over
                    self.selected_image = image
                    selection['image'] = image
                    break

    def load_images(self):
        images = load_images_from_spritesheet(self.filename)
        x = 10
        y = 100

        for i, image in enumerate(images):
            if y > height:
                x += res+10
                y = 100

            if self.resize:
                if self.scale:
                    image = pygame.transform.scale(image, (image.get_width()*self.scale, image.get_height()*self.scale))
                else:
                    image = pygame.transform.scale(image, (res, res))

            #Adds the images to the selector images list
            self.images.append(Image([x, y], image, self.id, i, self.autotile_config_path))

            y += image.get_height()+10

    def is_clicked(self, position):
        #Returns if the selector is clicked
        x, y = position

        return (
            x > self.position[0] and
            x < self.position[0] + self.get_width() and
            y > self.position[1] and
            y < self.position[1] + self.get_height()
        )

    def get_width(self):
        #Returns image width
        return self.label.get_width()

    def get_height(self):
        #Returns image height
        return self.label.get_height()
