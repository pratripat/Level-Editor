import json

from .ux.menu import Menu
from .funcs import resolve_path

class Menu_Manager:
    def __init__(self):
        self.menus = []

    def add_menu(self, filepath):
        try:
            data = json.load(open(filepath, 'r'))
            menu = Menu(data)
            self.menus.append(menu)
            return menu
        except Exception as e:
            print('=========================================')
            print(e)
            print(filepath, 'could not be loaded...')
            print('=========================================')

    def load_menus(self, filepath):
        try:
            menus = json.load(open(filepath, 'r'))

            for menu_data in menus:
                menu = Menu(menu_data)
                self.menus.append(menu)
        except Exception as e:
            print('=========================================')
            print(e)
            print(filepath, 'could not be loaded...')
            print('=========================================')

    def load_menu_positions(self, exception_ids=[]):
        self.menu_positions = json.load(open(resolve_path('data/configs/menu_positions.json'), 'r'))

        for menu_id in self.menu_positions:
            if menu_id not in exception_ids:
                rel_path = f'data/menus/{menu_id}.json'
                self.load_menus(resolve_path(rel_path))

        for menu in self.menus:
            menu.render_according_to_scroll = self.menu_positions[menu.id]['render_according_to_scroll']

    def render(self, screen, scroll=[0, 0]):
        for menu in self.menus:
            menu.render(screen, scroll)

    def update(self, scroll=[0, 0], key_inputs={'keys_pressed': [], 'keys_held': []}, mouse_inputs={'left': False, 'right': False, 'left_held': False, 'right_held': False, 'left_release': False, 'right_release': False}):
        for menu in self.menus:
            menu.update(scroll, key_inputs, mouse_inputs)

    def clear_menu_events(self):
        for menu in self.menus:
            menu.clear_events()

    def arrange_menus(self, order):
        arranged_menus = [None for _ in range(len(self.menus))]
        other_menus = []

        for i, menu_id in enumerate(order):
            if menu_id == '*':
                for menu in self.menus:
                    if menu.id not in order:
                        other_menus.append(menu)
                arranged_menus = arranged_menus[:i] + other_menus + arranged_menus[i+1:]
                continue

            menu = self.get_menu_with_id(menu_id)
            if menu:
                arranged_menus[i+len(other_menus)-1] = menu

        self.menus = [menu for menu in arranged_menus if menu != None]

    def get_selected_object(self):
        for menu in self.menus:
            if menu.selected_object:
                return menu.selected_object

    def get_menu_with_id(self, id):
        for menu in self.menus:
            if menu.id == id:
                return menu

        return None

    def get_menu_data(self, exception_ids=[]):
        data = [menu.get_data() for menu in self.menus if menu.id not in exception_ids]
        return data

    def update_menu_positions(self, window_size):
        for menu in self.menus:
            if self.menu_positions[menu.id]['position'][0] == 'right_edge':
                menu.position[0] = window_size[0]-menu.size[0]
            elif self.menu_positions[menu.id]['position'][0] == 'left_edge':
                menu.position[0] = 0
            if self.menu_positions[menu.id]['position'][1] == 'bottom_edge':
                menu.position[1] = window_size[1]-menu.size[1]
            elif self.menu_positions[menu.id]['position'][1] == 'top_edge':
                menu.position[1] = 0
            if self.menu_positions[menu.id]['position'][0] == 'center':
                menu.position[0] = window_size[0]//2-menu.size[0]//2
            if self.menu_positions[menu.id]['position'][1] == 'center':
                menu.position[1] = window_size[1]//2-menu.size[1]//2
            if isinstance(self.menu_positions[menu.id]['position'][0], int) and isinstance(self.menu_positions[menu.id]['position'][1], int):
                menu.position = self.menu_positions[menu.id]['position']
