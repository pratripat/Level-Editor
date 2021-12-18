from ..ui_component import UI_Component

class Button(UI_Component):
    def __init__(self, menu, data=None):
        super().__init__(menu, 'button', data)
