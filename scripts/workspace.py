import pygame
from .layer import Layer

class Workspace:
    TILE_SIZE = 32
    CHUNK_SIZE = 12

    def __init__(self, level_editor):
        self.level_editor = level_editor
        self.layers = {}
        self.tiles = {}
        self.scroll = [0,0]
        self.current_layer_index = 0
        self.current_tile_index = 0

    def render(self):
        for layer in self.layers.values():
            layer.render()

        if self.current_tile:
            self.level_editor.screen.blit(self.current_tile.image, (210, 10))

            if self.level_editor.input_system.mouse_states['left_held']:
                self.current_layer.add_tile(self.current_tile)

    def update(self):
        if self.level_editor.layers_menu.selected_object and self.level_editor.layers_menu.selected_object.object_id == 'textbox' and self.level_editor.layers_menu.selected_object.id != 'layers_title':
            self.current_layer_index = self.level_editor.layers_menu.textboxes.index(self.level_editor.layers_menu.selected_object)-1
            self.current_layer.id = self.level_editor.layers_menu.selected_object.text
            self.level_editor.tilemaps_menu.buttons = self.tiles[self.current_layer_index] + [self.level_editor.tilemaps_menu.get_object_with_id('add_tilemap')]

        if self.level_editor.tilemaps_menu.selected_object and self.level_editor.tilemaps_menu.selected_object.object_id == 'button' and self.level_editor.tilemaps_menu.selected_object.id != 'add_tilemap':
            self.current_tile_index = self.level_editor.tilemaps_menu.buttons.index(self.level_editor.tilemaps_menu.selected_object)-1

        if self.level_editor.layers_menu.is_mouse_hovering() or self.level_editor.tilemaps_menu.is_mouse_hovering():
            return

        self.current_layer.update()

    def add_layer(self):
        index = len(self.layers.values())
        self.layers[index] = Layer(f'layer_{index}', self.level_editor)

        if index not in self.tiles:
            self.tiles[index] = []

    def add_tilemap(self, tilemap):
        self.tiles[self.current_layer_index].append(tilemap)

    @property
    def current_layer(self):
        return self.layers[self.current_layer_index]

    @property
    def current_tile(self):
        try:
            return self.tiles[self.current_layer_index][self.current_tile_index]
        except:
            return None

    @property
    def visible_rect(self):
        return pygame.Rect(*self.scroll, *self.level_editor.window_size)
