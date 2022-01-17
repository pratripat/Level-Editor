import pygame

class Rectangle:
    def __init__(self, level_editor):
        self.level_editor = level_editor
        self.start_position = [None, None]
        self.end_position = [None, None]

    def render(self):
        if self.start_position == [None, None]:
            return

        scroll = self.level_editor.workspace.scroll
        if self.end_position == [None, None]:
            mouse_position = self.level_editor.input_system.mouse_position
            pygame.draw.rect(self.level_editor.screen, (242, 211, 171), (self.start_position[0]-scroll[0], self.start_position[1]-scroll[1], mouse_position[0]-self.start_position[0]+scroll[0], mouse_position[1]-self.start_position[1]+scroll[1]), 1)
        else:
            pygame.draw.rect(self.level_editor.screen, (242, 211, 171), (self.start_position[0]-scroll[0], self.start_position[1]-scroll[1], self.end_position[0]-self.start_position[0], self.end_position[1]-self.start_position[1]), 1)

    def set_start_position(self):
        self.start_position = self.level_editor.input_system.mouse_position.copy()
        self.start_position[0] += self.level_editor.workspace.scroll[0]
        self.start_position[1] += self.level_editor.workspace.scroll[1]
        self.end_position = [None, None]

    def set_end_position(self):
        if self.start_position == [None, None] or self.end_position != [None, None]:
            return

        self.end_position = self.level_editor.input_system.mouse_position.copy()
        self.end_position[0] += self.level_editor.workspace.scroll[0]
        self.end_position[1] += self.level_editor.workspace.scroll[1]

        if self.end_position == self.start_position:
            self.reset()

    def reset(self):
        self.start_position = self.end_position = [None, None]

    @property
    def formed(self):
        return self.end_position != [None, None]

    @property
    def rect(self):
        if self.formed:
            return pygame.Rect(*self.start_position, self.end_position[0]-self.start_position[0], self.end_position[1]-self.start_position[1])
        return pygame.Rect(0, 0, 0, 0)
