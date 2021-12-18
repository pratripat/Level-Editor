from tkinter import *
from tkinter import filedialog
from .input_system import Input
from .menu_manager import Menu_Manager

import pygame

pygame.init()

pygame.display.set_caption('Level Editor')

INITIAL_DIR = '/home/shubhendu/Documents/puttar/github-ssh/Level-Editor/data'

class Level_Editor:
    def __init__(self):
        self.window_size = (1000, 700)
        self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE+pygame.SCALED)

        self.input_system = Input()
        self.menu_manager = Menu_Manager()
        self.menu_manager.load_menu_positions(exception_ids=['load_tilemap_menu'])

        self.layers_menu = self.menu_manager.get_menu_with_id('layers_menu')
        self.tilemaps_menu = self.menu_manager.get_menu_with_id('tilemaps_menu')

        self.pop_up_menu = None

    def render(self):
        self.screen.fill((0, 0, 0))

        self.menu_manager.update_menu_positions(self.window_size)
        self.menu_manager.render(self.screen)

        pygame.display.update()

    def update(self):
        self.input_system.update()
        self.update_inputs()

        if self.pop_up_menu != None:
            self.pop_up_menu.update(key_inputs={'keys_pressed': self.input_system.keys_pressed, 'keys_held': self.input_system.keys_held}, mouse_inputs=self.input_system.mouse_states)
            return

        self.menu_manager.update(key_inputs={'keys_pressed': self.input_system.keys_pressed, 'keys_held': self.input_system.keys_held}, mouse_inputs=self.input_system.mouse_states)

    def update_inputs(self):
        if self.layers_menu.get_object_with_id('add_layer').id in self.layers_menu.events['button_click']:
            self.layers_menu.add_checkbox((25, 80+40*(len(self.layers_menu.textboxes)-1)), (175, 100+40*(len(self.layers_menu.textboxes)-1)))

        if 'add_tilemap' in self.tilemaps_menu.events['button_click']:
            self.menu_manager.load_menus('data/menus/load_tilemap_menu.json')
            self.pop_up_menu = self.menu_manager.get_menu_with_id('load_tilemap_menu')

        if self.pop_up_menu and self.pop_up_menu.id == 'load_tilemap_menu':
            if 'load_button' in self.pop_up_menu.events['button_click']:
                Tk().withdraw()
                filepath = filedialog.askopenfilename(initialdir = INITIAL_DIR, defaultextension = '.png', filetypes = [('PNG', '*.png')])
                if filepath != ():
                    image = pygame.image.load(filepath)
                    offset = self.tilemaps_menu.position
                    button = self.tilemaps_menu.add_button((25+offset[0], 80+offset[1]), (image.get_width()+offset[0], image.get_height()+offset[1]))
                    button.set_image_scale(1)
                    button.set_image(filepath)
                    self.menu_manager.menus.remove(self.pop_up_menu)
                    self.pop_up_menu = None
                    print('lol', button)

        self.menu_manager.clear_menu_events()

    def run(self):
        while 1:
            self.update()
            self.render()
