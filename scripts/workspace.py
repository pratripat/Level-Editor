import pygame
from .layer import Layer

class Workspace:
    def __init__(self, level_editor):
        self.level_editor = level_editor
        self.layers = {}
        self.scroll = [0,0]
        self.current_layer_index = 0

    def render(self):
        for layer in self.layers.values():
            layer.render()

    def update(self):
        if self.level_editor.layers_menu.selected_object and self.level_editor.layers_menu.selected_object.object_id == 'textbox' and self.level_editor.layers_menu.selected_object.id != 'layers_title':
            self.current_layer_index = self.level_editor.layers_menu.textboxes.index(self.level_editor.layers_menu.selected_object)-1
            self.current_layer.id = self.level_editor.layers_menu.selected_object.text

        if self.level_editor.layers_menu.is_mouse_hovering() or self.level_editor.tilemaps_menu.is_mouse_hovering():
            return

        self.current_layer.update()

    def add_layer(self):
        self.layers[len(self.layers.values())] = Layer(f'layer_{len(self.layers.values())}', self.level_editor)

    @property
    def current_layer(self):
        return self.layers[self.current_layer_index]

    @property
    def visible_rect(self):
        return pygame.Rect(*self.scroll, *self.level_editor.window_size)
