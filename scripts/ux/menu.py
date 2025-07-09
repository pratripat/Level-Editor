import pygame, json

from .ui_components.button import Button
from .ui_components.textbox import TextBox
from .ui_components.checkbox import CheckBox
from .ui_components.radiobutton import RadioButton

from ..funcs import resolve_path

class Menu:
    def __init__(self, data=None):
        if not data:
            data = json.load(open(resolve_path('data/configs/default/menu.json'), 'r'))

        self.is_menu = True
        self.object_id = 'menu'

        #PROPERTIES
        self.id = data['id']
        self.position = data['position']
        self.size = data['size']
        self.centered = data['centered']
        self.render_according_to_scroll = True

        # #STYLE
        self.background_color = tuple(data['background_color'])
        self.border_color = tuple(data['border_color'])
        self.border_width = data['border_width']
        self.border_radius = data['border_radius']
        self.opacity = data['opacity']

        self.buttons = self.load_buttons(data['buttons'])
        self.textboxes = self.load_textboxes(data['textboxes'])
        self.checkboxes = self.load_checkboxes(data['checkboxes'])
        self.radiobuttons = self.load_radiobuttons(data['radiobuttons'])

        # self.sub_menus = data['sub_menus']
        self.events = {'button_click': [], 'textbox_click': [], 'checkbox_click': [], 'radiobutton_click': []}

        self.selected_object = None

    def load_buttons(self, buttons_data):
        buttons = []

        for data in buttons_data:
            button = Button(self, data)
            buttons.append(button)

        return buttons

    def load_textboxes(self, textboxes_data):
        textboxes = []

        for data in textboxes_data:
            textbox = TextBox(self, data)
            textboxes.append(textbox)

        return textboxes

    def load_checkboxes(self, checkboxes_data):
        checkboxes = []

        for data in checkboxes_data:
            checkbox = CheckBox(self, data)
            checkboxes.append(checkbox)

        return checkboxes

    def load_radiobuttons(self, radiobuttons_data):
        radiobuttons = []

        for data in radiobuttons_data:
            radiobutton = RadioButton(self, data)
            radiobuttons.append(radiobutton)

        return radiobuttons

    def render(self, screen, scroll=[0,0]):
        scroll = self.get_scroll(scroll)

        surface = pygame.Surface(self.size)
        surface.set_colorkey((0,0,0))

        pygame.draw.rect(surface, self.background_color, [0, 0, *self.size], border_radius=self.border_radius)
        pygame.draw.rect(surface, self.border_color, [0, 0, *self.size], width=self.border_width, border_radius=self.border_radius)

        surface.set_alpha(self.opacity/100*255)

        offset = [0, 0]
        if self.centered:
            offset = [self.size[0]/2, self.size[1]/2]

        position = [self.position[0]-offset[0]-scroll[0], self.position[1]-offset[1]-scroll[1]]

        screen.blit(surface, position)

        for object in self.objects:
            object.render(screen, scroll)

        if self.selected_object:
            self.selected_object.highlight(screen, scroll)

    def update(self, scroll=[0,0], key_inputs={'keys_pressed': [], 'keys_held': []}, mouse_inputs={'left': False, 'right': False, 'left_held': False, 'right_held': False, 'left_release': False, 'right_release': False}):
        scroll = self.get_scroll(scroll)

        for object in self.objects:
            object.update(scroll, mouse_inputs)
            if object.is_clicked(scroll, mouse_inputs):
                self.selected_object = object

        if self.selected_object:
            self.selected_object.check_for_inputs(key_inputs)

        if len(self.events['radiobutton_click']) > 0:
            checked_radiobutton_id = self.events['radiobutton_click'][-1]
            for radiobutton in self.radiobuttons:
                if radiobutton.id != checked_radiobutton_id:
                    radiobutton.checked = False

    def clear_events(self):
        self.events = {'button_click': [], 'textbox_click': [], 'checkbox_click': [], 'radiobutton_click': []}

    def send_event(self, event_type, object_id):
        self.events[event_type].append(object_id)

    def add_button(self, start_position, end_position):
        button = Button(self)
        button.offset = [start_position[0]-self.position[0], start_position[1]-self.position[1]]
        button.size = [end_position[0]-start_position[0], end_position[1]-start_position[1]]

        if 0 in button.size:
            return None

        if button.size[0] < 0:
            button.offset[0] += button.size[0]
            button.size[0] = abs(button.size[0])
        if button.size[1] < 0:
            button.offset[1] += button.size[1]
            button.size[1] = abs(button.size[1])

        if button.id in [b.id for b in self.buttons]:
            button.id += str(len(self.buttons))

        self.buttons.append(button)
        return button

    def add_textbox(self, start_position, end_position):
        textbox = TextBox(self)
        textbox.offset = [start_position[0]-self.position[0], start_position[1]-self.position[1]]
        textbox.size = [end_position[0]-start_position[0], end_position[1]-start_position[1]]

        if 0 in textbox.size:
            return None

        if textbox.size[0] < 0:
            textbox.offset[0] += textbox.size[0]
            textbox.size[0] = abs(textbox.size[0])
        if textbox.size[1] < 0:
            textbox.offset[1] += textbox.size[1]
            textbox.size[1] = abs(textbox.size[1])

        if textbox.id in [b.id for b in self.textboxes]:
            textbox.id += str(len(self.textboxes))

        self.textboxes.append(textbox)
        return textbox

    def add_checkbox(self, start_position, end_position):
        checkbox = CheckBox(self)
        checkbox.offset = [start_position[0]-self.position[0], start_position[1]-self.position[1]]
        checkbox.size = [end_position[0]-start_position[0], end_position[1]-start_position[1]]

        if 0 in checkbox.size:
            return None

        if checkbox.size[0] < 0:
            checkbox.offset[0] += checkbox.size[0]
            checkbox.size[0] = abs(checkbox.size[0])
        if checkbox.size[1] < 0:
            checkbox.offset[1] += checkbox.size[1]
            checkbox.size[1] = abs(checkbox.size[1])

        if checkbox.id in [b.id for b in self.checkboxes]:
            checkbox.id += str(len(self.checkboxes))

        self.checkboxes.append(checkbox)
        return checkbox

    def add_radiobutton(self, start_position, end_position):
        radiobutton = RadioButton(self)
        radiobutton.offset = [start_position[0]-self.position[0], start_position[1]-self.position[1]]
        radiobutton.size = [end_position[0]-start_position[0], end_position[1]-start_position[1]]

        if 0 in radiobutton.size:
            return None

        if radiobutton.size[0] < 0:
            radiobutton.offset[0] += radiobutton.size[0]
            radiobutton.size[0] = abs(radiobutton.size[0])
        if radiobutton.size[1] < 0:
            radiobutton.offset[1] += radiobutton.size[1]
            radiobutton.size[1] = abs(radiobutton.size[1])

        if radiobutton.id in [b.id for b in self.radiobuttons]:
            radiobutton.id += str(len(self.radiobuttons))

        self.radiobuttons.append(radiobutton)
        return radiobutton

    def change_object_attr(self, object_id, attribute, value):
        for object in self.objects:
            if object.id == object_id:
                try:
                    setattr(object, attribute, value)
                except Exception as e:
                    print(e)
                    print('attribute setting error.')

    def get_scroll(self, scroll):
        if self.render_according_to_scroll:
            return scroll
        return [0,0]

    def get_data(self):
        return {
            'id': self.id,
            'position': self.position,
            'size': self.size,
            'centered': self.centered,
            'background_color': self.background_color,
            'border_color': self.border_color,
            'border_width': self.border_width,
            'border_radius': self.border_radius,
            'opacity': self.opacity,
            "buttons": [button.get_data() for button in self.buttons],
            "textboxes": [textbox.get_data() for textbox in self.textboxes],
            "checkboxes": [checkbox.get_data() for checkbox in self.checkboxes],
            "radiobuttons": [radiobutton.get_data() for radiobutton in self.radiobuttons]
        }

    def get_object_with_id(self, id):
        for object in self.objects:
            if object.id == id:
                return object

        return None

    def get_checked_radiobutton(self):
        for radiobutton in self.radiobuttons:
            if radiobutton.checked:
                return radiobutton

    def is_mouse_hovering(self, scroll=[0,0]):
        scroll = self.get_scroll(scroll)

        mouse_pos = pygame.mouse.get_pos()

        return (
            self.position[0]-self.render_offset[0] < mouse_pos[0]+scroll[0] < self.position[0]-self.render_offset[0]+self.size[0] and
            self.position[1]-self.render_offset[1] < mouse_pos[1]+scroll[1] < self.position[1]-self.render_offset[1]+self.size[1]
        )

    def is_clicked(self, scroll=[0,0], mouse_inputs={'left': False, 'right': False, 'left_held': False, 'right_held': False, 'left_release': False, 'right_release': False}):
        return self.is_mouse_hovering(scroll) and mouse_inputs['left']

    @property
    def objects(self):
        return [*self.buttons, *self.textboxes, *self.checkboxes, *self.radiobuttons]

    @property
    def render_offset(self):
        if self.centered:
            return [self.size[0]/2, self.size[1]/2]
        return [0, 0]
