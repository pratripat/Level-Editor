import pygame, json
from .layer import Layer
from .rectangle import Rectangle

class Workspace:
    TILE_RES = 64
    CHUNK_SIZE = 16

    def __init__(self, level_editor):
        self.level_editor = level_editor
        self.layers = {}
        self.tiles = {}
        self.scroll = [0,0]
        self.current_layer_index = 0
        self.current_tile = None

        self.rectangle = Rectangle(self.level_editor)

    def render(self):
        for layer in self.layers.values():
            layer.render()

        if self.current_tile:
            self.level_editor.screen.blit(self.current_tile.image, (210, 10))
            self.current_tile.highlight(self.level_editor.screen)

        self.rectangle.render()

    def update(self):
        self.handle_inputs()

        if self.level_editor.layers_manager.menu.selected_object and self.level_editor.layers_manager.menu.selected_object.object_id == 'textbox' and self.level_editor.layers_manager.menu.selected_object.id != 'layers_title':
            self.current_layer_index = self.level_editor.layers_manager.menu.textboxes.index(self.level_editor.layers_manager.menu.selected_object)-1
            self.current_layer.id = self.level_editor.layers_manager.menu.selected_object.text
            self.level_editor.tilemaps_manager.menu.buttons = [tile[0] for tile in self.tiles[self.current_layer_index]] + [self.level_editor.tilemaps_manager.menu.get_object_with_id('add_tilemap')]
            self.current_tile = None

        if self.level_editor.tilemaps_manager.menu.selected_object and self.level_editor.tilemaps_manager.menu.selected_object.object_id == 'button' and self.level_editor.tilemaps_manager.menu.selected_object.id != 'add_tilemap':
            #TODO
            # self.current_tile_index = self.level_editor.tilemaps_manager.menu.buttons.index(self.level_editor.tilemaps_manager.menu.selected_object)-1
            self.current_tile = self.level_editor.tilemaps_manager.menu.selected_object

        if self.level_editor.layers_manager.menu.is_mouse_hovering() or self.level_editor.tilemaps_manager.menu.is_mouse_hovering():
            return

        self.current_layer.update()

    def handle_inputs(self):
        if self.level_editor.input_system.mouse_states['right']:
            self.rectangle.set_start_position()
        elif self.level_editor.input_system.mouse_states['right_release']:
            self.rectangle.set_end_position()

        if self.level_editor.input_system.mouse_states['left']:
            self.rectangle.reset()

        if pygame.K_DELETE in self.level_editor.input_system.keys_pressed and self.rectangle.formed:
            self.current_layer.remove_tiles(self.get_tiles_within_rect())

        if self.current_tile:
            if self.level_editor.input_system.mouse_states['left_held'] and any([key in self.level_editor.input_system.keys_held for key in [pygame.K_LSHIFT, pygame.K_RSHIFT]]):
                self.current_layer.remove_tile([self.level_editor.input_system.mouse_position[0]+self.level_editor.workspace.scroll[0], self.level_editor.input_system.mouse_position[1]+self.level_editor.workspace.scroll[1]])
            elif self.level_editor.input_system.mouse_states['left_held'] and not any([menu.is_mouse_hovering() for menu in [self.level_editor.layers_manager.menu, self.level_editor.tilemaps_manager.menu]]):
                self.current_layer.add_tile(*self.current_tile_data)
            if self.level_editor.input_system.mouse_states['left'] and any([key in self.level_editor.input_system.keys_held for key in [pygame.K_LCTRL, pygame.K_RCTRL]]):
                self.current_layer.fill([self.level_editor.input_system.mouse_position[0]+self.level_editor.workspace.scroll[0], self.level_editor.input_system.mouse_position[1]+self.level_editor.workspace.scroll[1]])

        if not self.level_editor.layers_manager.menu.selected_object:
            if pygame.K_w in self.level_editor.input_system.keys_held:
                self.scroll[1] -= 10 * self.level_editor.fps * self.level_editor.dt
            if pygame.K_a in self.level_editor.input_system.keys_held:
                self.scroll[0] -= 10 * self.level_editor.fps * self.level_editor.dt
            if pygame.K_s in self.level_editor.input_system.keys_held:
                self.scroll[1] += 10 * self.level_editor.fps * self.level_editor.dt
            if pygame.K_d in self.level_editor.input_system.keys_held:
                self.scroll[0] += 10 * self.level_editor.fps * self.level_editor.dt

        if pygame.K_s in self.level_editor.input_system.keys_pressed and any([key in self.level_editor.input_system.keys_held for key in [pygame.K_LCTRL, pygame.K_RCTRL]]):
            filename = self.level_editor.ask_save_filename()
            if filename != ():
                self.save(filename)

    def add_layer(self):
        index = len(self.layers.values())
        self.layers[index] = Layer(f'layer_{index}', self.level_editor)

        if index not in self.tiles:
            self.tiles[index] = []

    def add_tilemap(self, tilemap, filepath, index):
        self.tiles[self.current_layer_index].append([tilemap, filepath, index])

    def get_tiles_within_rect(self):
        return self.current_layer.get_tiles_within_rect(self.rectangle.rect)

    def save(self, filename):
        data = {i:layer.get_data() for i, layer in enumerate(self.layers.values())}
        json.dump(data, open(filename, 'w'))

    @property
    def current_layer(self):
        return self.layers[self.current_layer_index]

    @property
    def current_tile_data(self):
        try:
            for tile_data in self.tiles[self.current_layer_index]:
                if tile_data[0] == self.current_tile:
                    return tile_data
        except:
            return None

    @property
    def visible_rect(self):
        return pygame.Rect(*self.scroll, *self.level_editor.window_size)
