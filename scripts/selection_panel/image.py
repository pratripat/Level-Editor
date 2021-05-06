class Image:
    def __init__(self, editor, id, position, image, autotile_config):
        self.editor = editor
        self.id = id
        self.position = position
        self.image = image
        self.autotile_config = autotile_config

    def render(self):
        self.editor.screen.blit(self.image, self.position)
