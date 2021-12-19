import pygame

from ..ui_component import UI_Component

class TextBox(UI_Component):
    def __init__(self, menu, data=None):
        super().__init__(menu, 'textbox', data)

    def update(self, scroll=[0,0], mouse_inputs={'left': False, 'right': False, 'left_held': False, 'right_held': False, 'left_release': False, 'right_release': False}):
        super().update(scroll, mouse_inputs)

    def check_for_inputs(self, key_inputs={'keys_pressed': [], 'keys_held': []}):
        if not self.interactable:
            return

        for key in key_inputs['keys_pressed']:
            caps_lock_key = pygame.KMOD_CAPS and pygame.key.get_mods()
            shift_key = (pygame.KMOD_LSHIFT or pygame.KMOD_RSHIFT) and pygame.key.get_mods()

            key_name = pygame.key.name(key)

            if key_name == 'backspace':
                self.text = self.text[:-1]
            elif key_name == 'space':
                self.text += ' '
            elif key_name == 'return':
                self.text += '\r'
            elif key_name in [letter for letter in 'abcdefghijklmnopqrstuvwxyz0123456789,./;[]=-'+"'"]:
                shift = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ)!@#$%^&*(<>?:{}+_"'
                caps_lock = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                index = [letter for letter in 'abcdefghijklmnopqrstuvwxyz0123456789,./;[]=-'+"'"].index(key_name)

                if shift_key:
                    self.text += shift[index]
                elif caps_lock_key and index < len(caps_lock):
                    self.text += caps_lock[index]
                else:
                    self.text += key_name
            else:
                print(key_name, 'was not added to the text...')
