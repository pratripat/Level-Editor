import pygame, json

from ..font_renderer import Font

class UI_Component:
    def __init__(self, menu, object_id, data=None):
        self.menu = menu

        if not data:
            data = json.load(open('data/configs/default/'+object_id+'.json', 'r'))

        self.is_menu = False

        #PROPERTIES
        self.id = data['id']
        self.text = data['text']
        self.offset = data['offset']
        self.size = data['size']
        self.centered = data['centered']
        self.object_id = object_id

        #STYLE
        self.background_color = data['background_color']
        self.border_color = data['border_color']
        self.hover_color = data['hover_color']
        self.border_width = data['border_width']
        self.border_radius = data['border_radius']
        self.opacity = data['opacity']

        #IMAGE
        self.original_image = None
        self.image_filepath = None
        self.image_scale = data['image_scale']

        #TEXT
        self.font = None
        self.font_filename = None
        self.font_color = data['font_color']
        self.font_scale = data['font_scale']
        self.font_background = data['font_background']
        self.font_opacity = data['font_opacity']
        self.interactable = data['interactable']

        self.current_color = self.background_color
        self.load_font(data['font'])
        self.set_image(data['image'])

    def render(self, screen, scroll=[0,0]):
        surface = pygame.Surface(self.size)
        surface.set_colorkey((0,0,0))

        pygame.draw.rect(surface, self.current_color, [0, 0, *self.size], border_radius=self.border_radius)
        pygame.draw.rect(surface, self.border_color, [0, 0, *self.size], width=self.border_width, border_radius=self.border_radius)

        surface.set_alpha(self.opacity/100*255)

        screen.blit(surface, [self.position[0]-self.render_offset[0]-scroll[0], self.position[1]-self.render_offset[1]-scroll[1]])

        if self.original_image:
            screen.blit(self.image, [self.position[0]+self.size[0]/2-self.image.get_width()/2-self.render_offset[0]-scroll[0], self.position[1]+self.size[1]/2-self.image.get_height()/2-self.render_offset[1]-scroll[1]])

        if self.font:
            alpha = self.font_opacity/100*255
            self.font.render(screen, self.text, [self.font_position[0]-self.render_offset[0]-scroll[0], self.font_position[1]-self.render_offset[1]-scroll[1]], center=(True, True), scale=self.font_scale, color=self.font_color, background_color=self.font_background, alpha=alpha, font_wrapping_width=self.size[0]-20)

    def highlight(self, screen, scroll=[0,0]):
        if not self.interactable:
            return

        pygame.draw.rect(screen, self.border_color, [self.position[0]-self.render_offset[0]-scroll[0]-5, self.position[1]-self.render_offset[1]-scroll[1]-5, self.size[0]+10, self.size[1]+10], width=2, border_radius=self.border_radius)

    def update(self, scroll=[0,0], mouse_inputs={'left': False, 'right': False, 'left_held': False, 'right_held': False, 'left_release': False, 'right_release': False}):
        if self.is_mouse_hovering(scroll):
            self.current_color = self.hover_color
        else:
            self.current_color = self.background_color

        if self.is_clicked(scroll, mouse_inputs):
            self.menu.send_event(f'{self.object_id}_click', self.id)

    def check_for_inputs(self, keys=[]):
        pass

    def is_mouse_hovering(self, scroll=[0,0]):
        mouse_pos = pygame.mouse.get_pos()

        return (
            self.position[0]-self.render_offset[0] < mouse_pos[0]+scroll[0] < self.position[0]-self.render_offset[0]+self.size[0] and
            self.position[1]-self.render_offset[1] < mouse_pos[1]+scroll[1] < self.position[1]-self.render_offset[1]+self.size[1]
        )

    def is_clicked(self, scroll=[0,0], mouse_inputs={'left': False, 'right': False, 'left_held': False, 'right_held': False, 'left_release': False, 'right_release': False}):
        if mouse_inputs['left']:
            if self.is_mouse_hovering(scroll):
                self.menu.selected_object = self
                return True
            elif not self.menu.is_clicked(scroll, mouse_inputs):
                self.menu.selected_object = None
            return False

    def load_font(self, font_filename):
        try:
            image = pygame.image.load(font_filename).convert()
        except:
            print(font_filename, 'could not be loaded..')
            return

        self.font = Font(font_filename)
        self.font_filename = font_filename

    def set_image(self, filepath):
        if filepath == None:
            return

        try:
            image = pygame.image.load(filepath).convert()
        except:
            print('could not load image. filepath: ', filepath)
            return

        self.image_filepath = filepath
        self.original_image = image

    def set_image_scale(self, scale):
        self.image_scale = scale

    def get_font_background(self):
        if self.font_background == None:
            return [0, 0, 0]
        return self.font_background

    def get_data(self):
        return {
            'id': self.id,
            'text': self.text,
            'offset': self.offset,
            'size': self.size,
            'centered': self.centered,
            'background_color': self.background_color,
            'border_color': self.border_color,
            'hover_color': self.hover_color,
            'border_width': self.border_width,
            'border_radius': self.border_radius,
            'opacity': self.opacity,
            'image': self.image_filepath,
            'image_scale': self.image_scale,
            'font': self.font_filename,
            'font_color': self.font_color,
            'font_scale': self.font_scale,
            'font_background': self.font_background,
            'font_opacity': self.font_opacity,
            'interactable': self.interactable
        }

    @property
    def position(self):
        return [self.menu.position[0]+self.offset[0], self.menu.position[1]+self.offset[1]]

    @property
    def font_position(self):
        return [self.position[0]+self.size[0]/2, self.position[1]+self.size[1]/2]

    @property
    def render_offset(self):
        if self.centered:
            return [self.size[0]/2, self.size[1]/2]
        return [0, 0]

    @property
    def image(self):
        if self.original_image:
            image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width()*self.image_scale), int(self.original_image.get_height()*self.image_scale)))
            image.set_colorkey((0,0,0))
            return image
        return self.original_image
