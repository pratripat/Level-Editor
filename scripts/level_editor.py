from .funcs import load_images_from_spritesheet
from tkinter import *
from tkinter import filedialog
from .input_system import Input
from .menu_manager import Menu_Manager
from .workspace import Workspace
from .menus.layers_manager import Layers_Manager
from .menus.tilemaps_manager import Tilemaps_Manager

import pygame

pygame.init()

pygame.display.set_caption('Level Editor')

INITIAL_DIR = '/home/shubhendu/Documents/puttar/github-ssh/Pawns-Gambit/data/graphics/spritesheet'

class Level_Editor:
    def __init__(self):
        self.window_size = (1000, 700)
        self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE+pygame.SCALED)

        self.input_system = Input()
        self.menu_manager = Menu_Manager()
        self.menu_manager.load_menu_positions(exception_ids=['load_tilemap_menu'])

        self.layers_manager = Layers_Manager(self)
        self.tilemaps_manager = Tilemaps_Manager(self)

        self.workspace = Workspace(self)

        self.pop_up_menu = None

        self.workspace.add_layer()
        textbox = self.layers_manager.menu.add_textbox((25, 80+40*(len(self.layers_manager.menu.textboxes)-1)), (175, 100+40*(len(self.layers_manager.menu.textboxes)-1)))
        textbox.text = f'layer_{len(self.workspace.layers.values())}'

        self.clock = pygame.time.Clock()
        self.fps = 100

    def render(self):
        self.screen.fill((0, 0, 0))

        self.workspace.render()
        self.menu_manager.render(self.screen)

        pygame.display.update()

    def update(self):
        self.clock.tick(self.fps)

        self.input_system.update()

        self.workspace.update()
        self.menu_manager.update_menu_positions(self.window_size)

        self.update_inputs()

        if self.pop_up_menu != None:
            self.pop_up_menu.update(key_inputs={'keys_pressed': self.input_system.keys_pressed, 'keys_held': self.input_system.keys_held}, mouse_inputs=self.input_system.mouse_states)
            return

        self.menu_manager.update(key_inputs={'keys_pressed': self.input_system.keys_pressed, 'keys_held': self.input_system.keys_held}, mouse_inputs=self.input_system.mouse_states)

    def update_inputs(self):
        self.layers_manager.update_inputs()
        self.tilemaps_manager.update_inputs()

        if self.pop_up_menu:
            if self.pop_up_menu.id == 'load_tilemap_menu':
                if self.pop_up_menu.get_checked_radiobutton() == None:
                    self.pop_up_menu.radiobuttons[0].checked = True

                if 'load_button' in self.pop_up_menu.events['button_click']:
                    Tk().withdraw()
                    filepath = filedialog.askopenfilename(initialdir = INITIAL_DIR, defaultextension = '.png', filetypes = [('PNG', '*.png')])
                    if filepath != ():
                        checked_radiobutton_id = self.pop_up_menu.get_checked_radiobutton().id

                        image_scale = ''.join(i for i in self.pop_up_menu.get_object_with_id('scale_textbox').text if i.isdigit() or i == '.')
                        if image_scale == '' or image_scale == '.': image_scale = '1'
                        image_scale = float(image_scale)

                        if checked_radiobutton_id == 'image_radiobutton':
                            image = pygame.image.load(filepath)
                            images = [image]
                            index = None
                        elif checked_radiobutton_id == 'spritesheet_radiobutton':
                            images = load_images_from_spritesheet(filepath)
                            index = 0

                        for i, image in enumerate(images):
                            if index != None:
                                index = i

                            offset = self.tilemaps_manager.menu.position.copy()
                            offset[1] += sum([button.size[1] for button in self.tilemaps_manager.menu.buttons if button.id != 'add_tilemap']) + 10*(len(self.tilemaps_manager.menu.buttons)-1)

                            button = self.tilemaps_manager.menu.add_button((25+offset[0], 80+offset[1]), (25+(image.get_width()*image_scale)+offset[0], 80+(image.get_height()*image_scale)+offset[1]))
                            button.set_image_scale(image_scale)
                            button.set_image_with_surface(image)

                            self.workspace.add_tilemap(button, filepath, index)

                        self.menu_manager.menus.remove(self.pop_up_menu)
                        self.pop_up_menu = None
                        self.input_system.mouse_states['left_held'] = False

            if self.pop_up_menu and 'close_button' in self.pop_up_menu.events['button_click']:
                self.menu_manager.menus.remove(self.pop_up_menu)
                self.pop_up_menu = None
                self.input_system.mouse_states['left_held'] = False

        self.menu_manager.clear_menu_events()

    def run(self):
        while 1:
            self.update()
            self.render()

    @property
    def dt(self):
        return 1/(self.clock.get_fps()+0.000001)
