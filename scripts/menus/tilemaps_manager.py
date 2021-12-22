class Tilemaps_Manager:
    def __init__(self, level_editor):
        self.level_editor = level_editor
        self.menu = self.level_editor.menu_manager.get_menu_with_id('tilemaps_menu')

    def update_inputs(self):
        if 'add_tilemap' in self.menu.events['button_click']:
            self.level_editor.menu_manager.load_menus('data/menus/load_tilemap_menu.json')
            self.level_editor.pop_up_menu = self.level_editor.menu_manager.get_menu_with_id('load_tilemap_menu')
