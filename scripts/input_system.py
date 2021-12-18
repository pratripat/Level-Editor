import pygame, sys

class Input:
    def __init__(self):
        self.keys_pressed = []
        self.keys_held = []
        self.mouse_position = [0, 0]
        self.mouse_states = {
            'left': False,
            'right': False,
            'left_held': False,
            'right_held': False,
            'left_release': True,
            'right_release': True
        }

        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])

    def update(self):
        self.mouse_position = list(pygame.mouse.get_pos())
        self.keys_pressed.clear()
        self.mouse_states['left'] = self.mouse_states['right'] = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                self.keys_pressed.append(event.key)
                if event.key not in self.keys_held:
                    self.keys_held.append(event.key)

            if event.type == pygame.KEYUP:
                if event.key in self.keys_held:
                    self.keys_held.remove(event.key)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.mouse_states['left']:
                        self.mouse_states['left'] = False
                    else:
                        self.mouse_states['left'] = True

                    self.mouse_states['left_held'] = True
                    self.mouse_states['left_release'] = False
                if event.button == 3:
                    if self.mouse_states['right']:
                        self.mouse_states['right'] = False
                    else:
                        self.mouse_states['right'] = True

                    self.mouse_states['right_held'] = True
                    self.mouse_states['right_release'] = False

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_states['left'] = False
                    self.mouse_states['left_held'] = False
                    self.mouse_states['left_release'] = True
                if event.button == 3:
                    self.mouse_states['right'] = False
                    self.mouse_states['right_held'] = False
                    self.mouse_states['right_release'] = True
