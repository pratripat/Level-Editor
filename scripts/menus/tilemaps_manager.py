class Tilemaps_Manager:
    def __init__(self, level_editor):
        self.level_editor = level_editor
        self.menu = self.level_editor.menu_manager.get_menu_with_id('tilemaps_menu')

    def update_inputs(self):
        if 'add_tilemap' in self.menu.events['button_click']:
            self.level_editor.menu_manager.load_menus('data/menus/load_tilemap_menu.json')
            self.level_editor.pop_up_menu = self.level_editor.menu_manager.get_menu_with_id('load_tilemap_menu')

    def clear_buttons(self):
        for button in self.menu.buttons[:]:
            if button.id != 'add_tilemap':
                self.menu.buttons.remove(button)

    def add_buttons(self, images, index, filepath, image_scale):
        buttons = []
        offset = self.menu.position.copy()

        for button in self.menu.buttons:
            if button.image:
                offset[1] += button.image.get_height() + 10

                if offset[1]+button.image.get_height() > self.menu.get_object_with_id('add_tilemap').position[1]-self.menu.get_object_with_id('add_tilemap').size[1]:
                    offset[0] += max([button.size[0] for button in self.menu.buttons if button.id != 'add_tilemap']) + 10
                    offset[1] = self.menu.position[1]

        for i, image in enumerate(images):
            if index != None:
                index = i

            # button = self.menu.add_button((25+offset[0], 80+offset[1]), (25+int(image.get_width()*image_scale)+offset[0], 80+int(image.get_height()*image_scale)+offset[1]))
            button = self.menu.add_button((25+offset[0], 80+offset[1]), (25+image.get_width()+offset[0], 80+image.get_height()+offset[1]))
            button.set_image_scale(1)
            button.set_image_with_surface(image)
            buttons.append(button)

            self.level_editor.workspace.add_tilemap(button, filepath, index, image_scale)

            offset[1] += button.size[1] + 10

            if offset[1]+button.size[1]*2 > self.menu.get_object_with_id('add_tilemap').position[1]-self.menu.get_object_with_id('add_tilemap').size[1]:
                offset[0] += max([button.size[0] for button in self.menu.buttons if button.id != 'add_tilemap']) + 10
                offset[1] = self.menu.position[1]

        if self.level_editor.pop_up_menu:
            self.level_editor.menu_manager.menus.remove(self.level_editor.pop_up_menu)
            self.level_editor.pop_up_menu = None
        self.level_editor.input_system.mouse_states['left_held'] = False

        return buttons
