import pygame, os
from .group import Group

FOLDER_PATH = 'data/groups'

class Selection_Panel:
    def __init__(self, editor):
        self.editor = editor
        self.groups = []
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

    def render(self):
        pygame.draw.rect(self.editor.screen, (173,195,232), (0,0,300,self.editor.screen.get_height()))

        if not self.current_group:
            return

        self.current_group.render()
        self.current_group.render_name()

    def update(self):
        if not self.current_group:
            return

        self.current_group.update()
