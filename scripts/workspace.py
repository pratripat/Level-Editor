import pygame
from .layer import Layer

class Workspace:
    TILE_RES = 64
    CHUNK_SIZE = 16

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
            self.level_editor.screen.blit(self.current_tile[0].image, (210, 10))
            self.current_tile[0].highlight(self.level_editor.screen)

    def update(self):
        self.handle_inputs()

        if self.level_editor.layers_manager.menu.selected_object and self.level_editor.layers_manager.menu.selected_object.object_id == 'textbox' and self.level_editor.layers_manager.menu.selected_object.id != 'layers_title':
            self.current_layer_index = self.level_editor.layers_manager.menu.textboxes.index(self.level_editor.layers_manager.menu.selected_object)-1
            self.current_layer.id = self.level_editor.layers_manager.menu.selected_object.text
            self.level_editor.tilemaps_manager.menu.buttons = self.tiles[self.current_layer_index] + [self.level_editor.tilemaps_manager.menu.get_object_with_id('add_tilemap')]

        if self.level_editor.tilemaps_manager.menu.selected_object and self.level_editor.tilemaps_manager.menu.selected_object.object_id == 'button' and self.level_editor.tilemaps_manager.menu.selected_object.id != 'add_tilemap':
            self.current_tile_index = self.level_editor.tilemaps_manager.menu.buttons.index(self.level_editor.tilemaps_manager.menu.selected_object)-1

        if self.level_editor.layers_manager.menu.is_mouse_hovering() or self.level_editor.tilemaps_manager.menu.is_mouse_hovering():
            return

        self.current_layer.update()

    def handle_inputs(self):
        if self.current_tile:
            if self.level_editor.input_system.mouse_states['left_held'] and not any([menu.is_mouse_hovering() for menu in [self.level_editor.layers_manager.menu, self.level_editor.tilemaps_manager.menu]]):
                self.current_layer.add_tile(*self.current_tile)

        if pygame.K_w in self.level_editor.input_system.keys_held:
            self.scroll[1] -= 5 * self.level_editor.fps * self.level_editor.dt
        if pygame.K_a in self.level_editor.input_system.keys_held:
            self.scroll[0] -= 5 * self.level_editor.fps * self.level_editor.dt
        if pygame.K_s in self.level_editor.input_system.keys_held:
            self.scroll[1] += 5 * self.level_editor.fps * self.level_editor.dt
        if pygame.K_d in self.level_editor.input_system.keys_held:
            self.scroll[0] += 5 * self.level_editor.fps * self.level_editor.dt

    def add_layer(self):
        index = len(self.layers.values())
        self.layers[index] = Layer(f'layer_{index}', self.level_editor)

        if index not in self.tiles:
            self.tiles[index] = []

    def add_tilemap(self, tilemap, filepath, index):
        self.tiles[self.current_layer_index].append([tilemap, filepath, index])

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
