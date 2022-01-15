class Layers_Manager:
    def __init__(self, level_editor):
        self.level_editor = level_editor
        self.menu = self.level_editor.menu_manager.get_menu_with_id('layers_menu')

    def update_inputs(self):
        if self.menu.get_object_with_id('add_layer').id in self.menu.events['button_click']:
            self.level_editor.workspace.add_layer()
            self.add_textbox()

    def add_textbox(self):
        textbox = self.menu.add_textbox((25, 80+40*(len(self.menu.textboxes)-1)), (175, 100+40*(len(self.menu.textboxes)-1)))
        textbox.text = f'layer_{len(self.level_editor.workspace.layers.values())}'
        return textbox

    def clear_textboxes(self):
        for textbox in self.menu.textboxes[:]:
            if textbox.id != 'layers_title':
                self.menu.textboxes.remove(textbox)

    def get_current_layer(self):
        return self.menu.textboxes[self.level_editor.workspace.current_layer_index+1]

    def remove_layer(self, layer):
        if len(self.level_editor.workspace.layers) == 1:
            return

        if layer in self.menu.textboxes:
            self.menu.textboxes.remove(layer)
            self.level_editor.workspace.remove_current_layer()

    def arrange_layers(self):
        for layer_index in self.level_editor.workspace.layers.keys():
            textbox = self.menu.textboxes[layer_index+1]
            textbox.offset = [25-self.menu.position[0], 80+40*layer_index-self.menu.position[1]]
