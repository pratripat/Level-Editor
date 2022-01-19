class Tilemaps_Options_Manager:
    def __init__(self, level_editor):
        self.level_editor = level_editor
        self.menu = self.level_editor.menu_manager.get_menu_with_id('tilemaps_options_menu')

    def update_inputs(self):
        if self.menu.get_object_with_id('randomizer_checkbox').checked:
            self.level_editor.workspace.randomizing = True
        else:
            self.level_editor.workspace.randomizing = False

        if self.menu.get_object_with_id('autotiling_checkbox').checked:
            if not self.level_editor.workspace.grid_mode:
                self.menu.get_object_with_id('autotiling_checkbox').checked = False
                self.level_editor.workspace.autotiling = False
                return
            self.level_editor.workspace.autotiling = True
        else:
            self.level_editor.workspace.autotiling = False
