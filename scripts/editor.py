import pygame, sys
from .world.world import World
from .selection_panel.selection_panel import Selection_Panel
from .font_renderer import Font

class Editor:
    def __init__(self):
        pygame.display.set_caption('Level Editor')

        self.screen = pygame.display.set_mode((1000, 600), pygame.RESIZABLE)
        self.font = Font('data/graphics/spritesheet/font')
        self.world = World(self)
        self.selection_panel = Selection_Panel(self)

    def render(self):
        self.screen.fill((13,19,42))

        self.world.render()
        self.selection_panel.render()

        pygame.display.update()

    def run(self):
        pass

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def main_loop(self):
        while True:
            self.event_loop()
            self.run()
            self.render()
