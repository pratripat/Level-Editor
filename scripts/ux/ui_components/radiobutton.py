import pygame

from ..ui_component import UI_Component

class RadioButton(UI_Component):
    def __init__(self, menu, data=None):
        super().__init__(menu, 'radiobutton', data)

        self.checked = False
        self.just_clicked = False

    def render(self, screen, scroll=[0,0]):
        surface = pygame.Surface(self.size)
        surface.set_colorkey((0,0,0))

        pygame.draw.rect(surface, self.current_color, [0, 0, *self.size], border_radius=self.border_radius)
        pygame.draw.rect(surface, self.border_color, [0, 0, *self.size], width=self.border_width, border_radius=self.border_radius)

        pygame.draw.circle(surface, self.border_color, [self.size[1]//2, self.size[1]//2], self.size[1]//2-10, width=self.border_width)

        if self.checked:
            pygame.draw.circle(surface, self.border_color, [self.size[1]//2, self.size[1]//2], self.size[1]//2-10)

        surface.set_alpha(self.opacity/100*255)

        screen.blit(surface, [self.position[0]-self.render_offset[0]-scroll[0], self.position[1]-self.render_offset[1]-scroll[1]])

        if self.image:
            screen.blit(self.image, [self.position[0]+self.size[0]/2-self.image.get_width()/2-self.render_offset[0]-scroll[0], self.position[1]+self.size[1]/2-self.image.get_height()/2-self.render_offset[1]-scroll[1]])

        if self.font:
            alpha = self.font_opacity/100*255
            self.font.render(screen, self.text, [self.font_position[0]+self.size[1]-24-self.render_offset[0]-scroll[0], self.font_position[1]-self.render_offset[1]-scroll[1]], center=(True, True), scale=self.font_scale, color=self.font_color, background_color=self.font_background, alpha=alpha, font_wrapping_width=self.size[0]-self.size[1]-20)

    def update(self, scroll=[0,0], mouse_inputs={'left': False, 'right': False, 'left_held': False, 'right_held': False, 'left_release': False, 'right_release': False}):
        super().update(scroll, mouse_inputs)

        if self.is_clicked(scroll, mouse_inputs):
            if not self.just_clicked:
                self.checked = not self.checked
                self.just_clicked = True
        elif not mouse_inputs['left']:
            self.just_clicked = False
