class Tilemaps_Options_Manager:
    def __init__(self, level_editor):
        self.level_editor = level_editor
        self.menu = self.level_editor.menu_manager.get_menu_with_id('tilemaps_options_menu')

    def update_inputs(self):
        pass
