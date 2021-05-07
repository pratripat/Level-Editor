import pygame, os
from .group import Group
from ..button import Button

FOLDER_PATH = 'data/groups'

class Selection_Panel:
    def __init__(self, editor):
        self.editor = editor
        self.groups = []
        self.width = 300
        self.current_group = None
        self.current_group_index = None
        self.load()

    def load(self):
        for group in os.listdir(FOLDER_PATH):
            g = Group(FOLDER_PATH+'/'+group, group, self.editor)
            self.groups.append(g)

        if len(self.groups) > 0:
            self.current_group = self.groups[0]
            self.current_group_index = 0

        previous_button = Button({'x': 50, 'y':30, 'w':80, 'h':40},
            {'color':(13,19,42), 'hover_color':(13,19,42), 'font_color':(173,195,232), 'alpha':255},
            {'text':'Previous', 'font_renderer':self.editor.font}, type='previous')
        next_button = Button({'x': 250, 'y':30, 'w':80, 'h':40},
            {'color':(13,19,42), 'hover_color':(13,19,42), 'font_color':(173,195,232), 'alpha':255},
            {'text':'Next', 'font_renderer':self.editor.font}, type='next')
        self.buttons = [previous_button, next_button]

    def select_previous_group(self):
        if not self.current_group:
            return

        self.current_group_index -= 1
        self.current_group_index %= len(self.groups)
        self.current_group = self.groups[self.current_group_index]

    def select_next_group(self):
        if not self.current_group:
            return

        self.current_group_index += 1
        self.current_group_index %= len(self.groups)
        self.current_group = self.groups[self.current_group_index]

    def render(self):
        pygame.draw.rect(self.editor.screen, (173,195,232), (0,0,self.width,self.editor.screen.get_height()))

        for button in self.buttons:
            button.show(self.editor.screen, scale=0.7)

        if not self.current_group:
            return

        self.current_group.render()
        self.current_group.render_name()

    def update(self):
        for button in self.buttons:
            button.update()

        if not self.current_group:
            return

        self.current_group.update()

    def update_on_mouse_click(self, position):
        for button in self.buttons:
            if button.type == 'previous':
                button.on_click(self.select_previous_group)
            if button.type == 'next':
                button.on_click(self.select_next_group)

        if not self.current_group:
            return

        self.current_group.update_on_mouse_click(position)

    def get_current_selection(self):
        if not self.current_group:
            return

        return self.current_group.current_image

    def get_images_with_name(self, name):
        #Returns group's image if the group's name is the same as the given name
        for group in self.groups:
            if group.name == name:
                return group.images

        return []

    def is_mouse_hovering(self, pos):
        return (
            pos[0] < self.width
        )
