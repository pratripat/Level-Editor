class Layers_Options_Manager:
    def __init__(self, level_editor):
        self.level_editor = level_editor
        self.menu = self.level_editor.menu_manager.get_menu_with_id('layers_options_menu')

    def update_inputs(self):
        if 'layer_delete' in self.menu.events['button_click']:
            current_layer = self.level_editor.layers_manager.get_current_layer()
            self.level_editor.layers_manager.remove_layer(current_layer)

        if 'layer_up' in self.menu.events['button_click']:
            self.level_editor.workspace.move_current_layer_up()

        if 'layer_down' in self.menu.events['button_click']:
            self.level_editor.workspace.move_current_layer_down()
