import pygame

def load_images_from_spritesheet(filename):
    #Tries to load the file
    try:
        spritesheet = pygame.image.load(filename).convert()
    except Exception as e:
        print('LOADING SPRITESHEET ERROR: ', e)
        return []

    rows = []
    images = []

    for y in range(spritesheet.get_height()):
        pixil = spritesheet.get_at((0, y))
        if pixil[2] == 255:
            rows.append(y)

    for row in rows:
        for x in range(spritesheet.get_width()):
            start_position = []
            pixil = spritesheet.get_at((x, row))
            if pixil[0] == 255 and pixil[1] == 255 and pixil[2] == 0:
                start_position = [x+1, row+1]
                width = height = 0

                for rel_x in range(start_position[0], spritesheet.get_width()):
                    pixil = spritesheet.get_at((rel_x, start_position[1]))
                    if pixil[0] == 255 and pixil[1] == 0 and pixil[2] == 255:
                        width = rel_x - start_position[0]
                        break

                for rel_y in range(start_position[1], spritesheet.get_height()):
                    pixil = spritesheet.get_at((start_position[0], rel_y))
                    if pixil[0] == 255 and pixil[1] == 0 and pixil[2] == 255:
                        height = rel_y - start_position[1]
                        break

                image = pygame.Surface((width, height))
                image.set_colorkey((0,0,0))
                image.blit(spritesheet, (-start_position[0], -start_position[1]))

                images.append(image)

    return images

class Font:
    def __init__(self, filename):
        self.filename = filename
        self.characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@!-*.'
        self.space_width = 10
        self.load_characters()

    #Loads all the images from the spritesheet
    def load_characters(self):
        self.images = []
        images = load_images_from_spritesheet(self.filename)

        for image in images:
            self.images.append(image)

    #Returns the surface on which the text will be rendered
    def get_surface(self, text, font_wrapping_width=None):
        width = 0
        height = 0

        for chr in text:
            if chr in self.characters:
                index = self.characters.index(chr)
                image = self.images[index]

                width += image.get_width()

                if image.get_height() > height:
                    height = image.get_height()
            elif chr == ' ':
                width += self.space_width

        height_copy = height

        if font_wrapping_width and width > font_wrapping_width:
            height *= int(width/font_wrapping_width)+1
            width = font_wrapping_width

        for chr in text:
            if chr == '\r':
                height += height_copy

        surface = pygame.Surface((width, height))
        surface.set_colorkey((0,0,0))

        return surface

    #Changes the color of the text
    def change_color(self, surface, old_color, new_color):
        surface.set_colorkey(old_color)
        surf = surface.copy()
        surf.fill(new_color)
        surf.blit(surface, (0,0))
        return surf

    #Renders the text on the surface
    def render(self, screen, text, position, center=(False, False), scale=1, color=None, background_color=None, alpha=255, font_wrapping_width=None):
        font_wrapping_width = max(10, font_wrapping_width)

        text = text.upper()
        surface = self.get_surface(text, font_wrapping_width)
        surface = pygame.transform.scale(surface, (round(surface.get_width()*scale), round(surface.get_height()*scale)))
        temp_pos = [0,0]

        for chr in text:
            if chr == '\r':
                temp_pos[0] = 0
                temp_pos[1] += max([image.get_height() for image in self.images])
            if chr in self.characters:
                index = self.characters.index(chr)
                image = self.images[index]
                image = pygame.transform.scale(image, (round(image.get_width()*scale), round(image.get_height()*scale)))

                if temp_pos[0]+image.get_width() > surface.get_width():
                    temp_pos[0] = 0
                    temp_pos[1] += max([image.get_height() for image in self.images])

                surface.blit(image, temp_pos)

                temp_pos[0] += image.get_width()
            elif chr == ' ':
                temp_pos[0] += self.space_width

        if color:
            surface = self.change_color(surface, self.get_font_color(), color)
            surface.set_colorkey((0,0,0))

        if center[0]:
            position = [position[0]-surface.get_width()/2, position[1]]
        if center[1]:
            position = [position[0], position[1]-surface.get_height()/2]

        if background_color:
            background = pygame.Surface(surface.get_size())
            background.fill(background_color)
            screen.blit(background, position)

        surface.set_alpha(alpha)

        screen.blit(surface, position)

        return position

    def remove_unwanted_text(self, text):
        text = text.upper()

        for chr in text:
            if chr not in self.characters and chr not in [' ', '\r']:
                text = text.replace(chr, '')

        return text

    def get_font_color(self):
        character = self.images[0]

        for x in range(character.get_width()):
            for y in range(character.get_height()):
                pixel_color = character.get_at((x, y))
                if pixel_color[:3] != (0, 0, 0):
                    return pixel_color[:3]
