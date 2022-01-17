import os
from .font_renderer import Font
from .funcs import load_images_from_spritesheet
from tkinter import *
from tkinter import filedialog
from .input_system import Input
from .menu_manager import Menu_Manager
from .workspace import Workspace
from .menus.layers_manager import Layers_Manager
from .menus.layers_options_manager import Layers_Options_Manager
from .menus.tilemaps_options_manager import Tilemaps_Options_Manager
from .menus.tilemaps_manager import Tilemaps_Manager

import pygame

pygame.init()

pygame.display.set_caption('Level Editor')

INITIAL_DIR = '/home/shubhendu/Documents/puttar/github-ssh/Level-Editor/data'

class Level_Editor:
    def __init__(self):
        self.window_size = (1200, 700)
        self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)

        self.input_system = Input()
        self.menu_manager = Menu_Manager()
        self.menu_manager.load_menu_positions(exception_ids=['load_tilemap_menu'])

        self.layers_manager = Layers_Manager(self)
        self.layers_options_manager = Layers_Options_Manager(self)
        self.tilemaps_options_manager = Tilemaps_Options_Manager(self)
        self.tilemaps_manager = Tilemaps_Manager(self)
        self.workspace = Workspace(self)
        self.font = Font('data/graphics/font.png')

        self.absolute_filepath = os.path.abspath("..")

        self.pop_up_menu = None

        self.workspace.add_layer()
        self.layers_manager.add_textbox()

        self.clock = pygame.time.Clock()
        self.fps = 100

    def render(self):
        self.screen.fill((0, 0, 0))

        self.workspace.render()
        self.menu_manager.render(self.screen)

        self.font.render(self.screen, f'mouse position- {self.input_system.mouse_position}', [210, self.screen.get_height()-30], center=(False, False), scale=1.5, color=(245, 239, 126))
        self.font.render(self.screen, f'mouse position- {self.input_system.mouse_position}', [self.screen.get_width()-480, self.screen.get_height()-30], center=(False, False), scale=1.5, color=(245, 239, 126))

        pygame.display.update()

    def update(self):
        self.window_size = self.screen.get_size()

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
        self.layers_options_manager.update_inputs()
        self.tilemaps_options_manager.update_inputs()
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

                        autotile = self.pop_up_menu.get_object_with_id('autotile_checkbox').checked

                        self.tilemaps_manager.add_buttons(images, index, filepath, image_scale, autotile)

            if self.pop_up_menu and 'close_button' in self.pop_up_menu.events['button_click']:
                self.menu_manager.menus.remove(self.pop_up_menu)
                self.pop_up_menu = None
                self.input_system.mouse_states['left_held'] = False

        self.menu_manager.clear_menu_events()

    def run(self):
        while 1:
            self.update()
            self.render()

    def ask_save_filename(self):
        Tk().withdraw()
        return filedialog.asksaveasfilename(initialdir = INITIAL_DIR, defaultextension = '.json', filetypes = [('JSON', '*.json')])

    def ask_open_filename(self):
        Tk().withdraw()
        return filedialog.askopenfilename(initialdir = INITIAL_DIR, defaultextension = '.json', filetypes = [('JSON', '*.json')])

    @property
    def dt(self):
        return 1/(self.clock.get_fps()+0.000001)
