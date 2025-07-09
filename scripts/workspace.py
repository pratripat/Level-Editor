import pygame, random, json
from .funcs import load_images_from_spritesheet, resolve_path
from .layer import Layer
from .rectangle import Rectangle

class Workspace:
    TILE_RES = 48
    CHUNK_SIZE = 16

    def __init__(self, level_editor):
        self.level_editor = level_editor
        self.layers = {}
        self.tiles = {}
        self.scroll = [0,0]
        self.current_layer_index = 0
        self.current_tile = None
        self.randomizing = False
        self.autotiling = False
        self.grid_mode = True
        self.current_layer_mode = False

        self.rectangle = Rectangle(self.level_editor)

        self.autotile_filename = resolve_path('data/autotile/8_bit_autotiling.json')

    def render(self):
        if self.current_layer_mode:
            surface = pygame.Surface(self.level_editor.screen.get_size())
            surface.set_colorkey((0,0,0))
            surface.set_alpha(128)
            for layer in self.layers.values():
                layer.render(surface)
            self.level_editor.screen.blit(surface, (0,0))
            self.current_layer.render()
        else:
            for layer in self.layers.values():
                layer.render()

        self.render_hovering_tile()
        self.rectangle.render()

    def render_hovering_tile(self):
        if self.current_tile:
            image = self.current_tile.image
            image = pygame.transform.scale(image, (int(image.get_width() * self.current_tile_data[3]), int(image.get_height() * self.current_tile_data[3])))
            image.set_colorkey((0,0,0))
            image.set_alpha(100)
            position = [self.level_editor.input_system.mouse_position[0]+self.scroll[0], self.level_editor.input_system.mouse_position[1]+self.scroll[1]]

            if self.grid_mode:
                tile_position = [(position[0]//self.level_editor.workspace.TILE_RES)*self.level_editor.workspace.TILE_RES, (position[1]//self.level_editor.workspace.TILE_RES)*self.level_editor.workspace.TILE_RES]
            else:
                tile_position = position

            self.level_editor.screen.blit(image, [tile_position[0]-self.scroll[0], tile_position[1]-self.scroll[1]])

    def update(self):
        if not self.grid_mode:
            self.autotiling = False
            self.level_editor.tilemaps_options_manager.menu.get_object_with_id('autotiling_checkbox').checked = False

        self.handle_inputs()

        if self.level_editor.layers_manager.menu.selected_object and self.level_editor.layers_manager.menu.selected_object.object_id == 'textbox' and self.level_editor.layers_manager.menu.selected_object.id != 'layers_title':
            #OHO
            self.current_layer_index = self.level_editor.layers_manager.menu.textboxes.index(self.level_editor.layers_manager.menu.selected_object)-1
            self.current_layer.id = self.level_editor.layers_manager.menu.selected_object.text
            self.level_editor.tilemaps_manager.menu.buttons = [tile[0] for tile in self.tiles[self.current_layer]] + [self.level_editor.tilemaps_manager.menu.get_object_with_id('add_tilemap')]
            self.current_tile = None

        if self.level_editor.tilemaps_manager.menu.selected_object and self.level_editor.tilemaps_manager.menu.selected_object.object_id == 'button' and self.level_editor.tilemaps_manager.menu.selected_object.id != 'add_tilemap':
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
            if self.level_editor.input_system.mouse_states['left_held'] and not any([menu.is_mouse_hovering() for menu in self.level_editor.menu_manager.menus]):
                data = self.current_tile_data
                if self.randomizing:
                    data = self.random_tile_data

                tile = self.current_layer.add_tile(*data)

                if self.autotiling:
                    self.autotile(self.current_layer.get_tile_neighbors(tile)+[tile])

            if self.level_editor.input_system.mouse_states['left'] and any([key in self.level_editor.input_system.keys_held for key in [pygame.K_LCTRL, pygame.K_RCTRL]]):
                self.current_layer.fill([self.level_editor.input_system.mouse_position[0]+self.level_editor.workspace.scroll[0], self.level_editor.input_system.mouse_position[1]+self.level_editor.workspace.scroll[1]])

        if self.level_editor.input_system.mouse_states['left_held'] and any([key in self.level_editor.input_system.keys_held for key in [pygame.K_LSHIFT, pygame.K_RSHIFT]]):
            tiles = self.current_layer.remove_tile([self.level_editor.input_system.mouse_position[0]+self.level_editor.workspace.scroll[0], self.level_editor.input_system.mouse_position[1]+self.level_editor.workspace.scroll[1]])

            if self.autotiling and len(tiles):
                self.autotile(self.current_layer.get_tile_neighbors(tiles[0]))

        if not self.level_editor.layers_manager.menu.selected_object:
            if pygame.K_w in self.level_editor.input_system.keys_held:
                self.scroll[1] -= 10 * self.level_editor.fps * self.level_editor.dt
            if pygame.K_a in self.level_editor.input_system.keys_held:
                self.scroll[0] -= 10 * self.level_editor.fps * self.level_editor.dt
            if pygame.K_s in self.level_editor.input_system.keys_held:
                self.scroll[1] += 10 * self.level_editor.fps * self.level_editor.dt
            if pygame.K_d in self.level_editor.input_system.keys_held:
                self.scroll[0] += 10 * self.level_editor.fps * self.level_editor.dt

        if pygame.K_t in self.level_editor.input_system.keys_pressed and any([key in self.level_editor.input_system.keys_held for key in [pygame.K_LCTRL, pygame.K_RCTRL]]):
            self.autotile()

        if pygame.K_z in self.level_editor.input_system.keys_pressed and any([key in self.level_editor.input_system.keys_held for key in [pygame.K_LCTRL, pygame.K_RCTRL]]):
            self.current_layer.undo()

        if pygame.K_y in self.level_editor.input_system.keys_pressed and any([key in self.level_editor.input_system.keys_held for key in [pygame.K_LCTRL, pygame.K_RCTRL]]):
            self.current_layer.redo()

        if pygame.K_g in self.level_editor.input_system.keys_pressed and any([key in self.level_editor.input_system.keys_held for key in [pygame.K_LCTRL, pygame.K_RCTRL]]):
            self.grid_mode = not self.grid_mode

        if pygame.K_l in self.level_editor.input_system.keys_pressed and any([key in self.level_editor.input_system.keys_held for key in [pygame.K_LCTRL, pygame.K_RCTRL]]):
            self.current_layer_mode = not self.current_layer_mode

        if pygame.K_o in self.level_editor.input_system.keys_pressed and any([key in self.level_editor.input_system.keys_held for key in [pygame.K_LCTRL, pygame.K_RCTRL]]):
            filename = self.level_editor.ask_open_filename()
            if filename != () and filename != '':
                self.load(filename)

        if pygame.K_s in self.level_editor.input_system.keys_pressed and any([key in self.level_editor.input_system.keys_held for key in [pygame.K_LCTRL, pygame.K_RCTRL]]):
            filename = self.level_editor.ask_save_filename()
            if filename != () and filename != '':
                self.save(filename)

        if pygame.K_t in self.level_editor.input_system.keys_pressed and any([key in self.level_editor.input_system.keys_held for key in [pygame.K_LCTRL, pygame.K_RCTRL]]) and any([key in self.level_editor.input_system.keys_held for key in [pygame.K_LSHIFT, pygame.K_RSHIFT]]):
            filename = self.level_editor.ask_open_filename()
            if filename != () and filename != '':
                self.autotile_filename = filename
                print('NEW AUTOTILE FILE: ', self.autotile_filename)

    def add_layer(self):
        index = len(self.layers.values())
        layer = Layer(f'layer_{index+1}', self.level_editor)
        self.layers[index] = layer

        if layer not in self.tiles:
            self.tiles[layer] = []

        return index, layer

    def remove_current_layer(self):
        current_layer = self.layers[self.current_layer_index]
        del self.tiles[current_layer]
        del self.layers[self.current_layer_index]

        layers = {}
        for index in self.layers.keys():
            if index < self.current_layer_index:
                layers[index] = self.layers[index]
            else:
                layers[len(layers.values())] = self.layers[index]

        self.current_layer_index -= 1
        self.layers = layers

        if self.current_layer_index < 0:
            self.current_layer_index = list(self.layers.keys())[0]

        self.level_editor.layers_manager.arrange_layers()
        self.level_editor.tilemaps_manager.menu.buttons = [tile[0] for tile in self.tiles[self.current_layer]] + [self.level_editor.tilemaps_manager.menu.get_object_with_id('add_tilemap')]

    def move_current_layer_up(self):
        if len(self.layers) == 1:
            return

        target_layer_index = self.current_layer_index - 1
        if target_layer_index < 0:
            target_layer_index = list(self.layers.keys())[-1]

        current_layer = self.layers[self.current_layer_index]
        del self.layers[self.current_layer_index]

        layers = list(self.layers.values())
        layers = layers[:target_layer_index] + [current_layer] + layers[target_layer_index:]
        new_layers = {}

        for i, layer in enumerate(layers):
            new_layers[i] = layer

        self.layers = new_layers
        self.current_layer_index = target_layer_index

        self.level_editor.layers_manager.reorder_layers()

    def move_current_layer_down(self):
        if len(self.layers) == 1:
            return

        target_layer_index = self.current_layer_index + 1
        if target_layer_index > len(self.layers)-1:
            target_layer_index = list(self.layers.keys())[0]

        current_layer = self.layers[self.current_layer_index]
        del self.layers[self.current_layer_index]

        layers = list(self.layers.values())
        layers = layers[:target_layer_index] + [current_layer] + layers[target_layer_index:]
        new_layers = {}

        for i, layer in enumerate(layers):
            new_layers[i] = layer

        self.layers = new_layers
        self.current_layer_index = target_layer_index

        self.level_editor.layers_manager.reorder_layers()

    def autotile(self, autotile_tiles=None):
        tiles = self.get_tiles_within_rect()

        if self.autotiling and autotile_tiles:
            tiles = autotile_tiles

        self.current_layer.autotile(tiles)

    def add_tilemap(self, tilemap, filepath, spritesheet_index, image_scale):
        self.tiles[self.current_layer].append([tilemap, filepath, spritesheet_index, image_scale])

    def get_tiles_within_rect(self):
        return self.current_layer.get_tiles_within_rect(self.rectangle.rect)

    def save(self, filename):
        tilemaps = list(self.level_editor.tilemaps_manager.tilemaps.keys())
        data = {'layers': [layer.get_data(tilemaps) for layer in self.layers.values()], 'tilemaps': self.level_editor.tilemaps_manager.tilemaps}
        json.dump(data, open(filename, 'w'))

    def load(self, filename):
        #Loading layers
        self.tiles.clear()
        self.layers.clear()
        self.level_editor.layers_manager.clear_textboxes()
        self.level_editor.tilemaps_manager.clear_buttons()

        self.scroll = [0,0]
        self.current_layer_index = 0
        self.current_tile = None

        data = json.load(open(filename, 'r'))

        layers = data['layers']
        tilemaps = list(data['tilemaps'].keys())
        tilemap_types = {}

        for layer_data in layers:
            index, layer = self.add_layer()
            layer.id = layer_data[0]
            layer.load(layer_data[1], tilemaps)

            textbox = self.level_editor.layers_manager.add_textbox()
            textbox.text = layer_data[0]

            tilemap_types[layer_data[0]] = {'images': [], 'spritesheets': []}
            for tile_data in layer_data[1]:
                if tile_data[3] == None:
                    if [tilemaps[tile_data[2]], tile_data[4]] not in tilemap_types[layer_data[0]]['images']:
                        tilemap_types[layer_data[0]]['images'].append([tilemaps[tile_data[2]], tile_data[4]])
                else:
                    if [tilemaps[tile_data[2]], tile_data[4]] not in tilemap_types[layer_data[0]]['spritesheets']:
                        tilemap_types[layer_data[0]]['spritesheets'].append([tilemaps[tile_data[2]], tile_data[4]])

        #Loading tilemaps
        for i, tilemaps_data in enumerate(tilemap_types.values()):
            self.level_editor.tilemaps_manager.clear_buttons()
            self.current_layer_index = i
            images = []

            for tilemap in tilemaps_data['images']:
                index = None
                filepath = tilemap[0]
                image_scale = tilemap[1]
                image = pygame.image.load(filepath)
                image.set_colorkey((0,0,0))
                images = [image]

            for tilemap in tilemaps_data['spritesheets']:
                index = 0
                filepath = tilemap[0]
                image_scale = tilemap[1]
                images = load_images_from_spritesheet(filepath)

            if len(images):
                self.level_editor.tilemaps_manager.add_buttons(images, index, filepath, image_scale, data['tilemaps'][filepath])

    @property
    def random_tile_data(self):
        if self.current_tile:
            tiles = self.tiles[self.current_layer]
            same_file_tiles = [tile for tile in tiles if tile[1] == self.current_tile_data[1]]
            return random.choice(same_file_tiles)

    @property
    def current_layer(self):
        return self.layers[self.current_layer_index]

    @property
    def current_tile_data(self):
        try:
            for tile_data in self.tiles[self.current_layer]:
                if tile_data[0] == self.current_tile:
                    return tile_data
        except:
            return None

    @property
    def visible_rect(self):
        return pygame.Rect(*self.scroll, *self.level_editor.window_size)
