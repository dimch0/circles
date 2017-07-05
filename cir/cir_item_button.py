#######################################################################################################################
#################                                                                                     #################
#################                                 Button class                                        #################
#################                                                                                     #################
#######################################################################################################################
from cir_item import Item

class ButtonItem(Item):
    """
    This is the base class for all CIR items
    """
    def __init__(self, font=None, text_color=None, **kwargs):
        super(ButtonItem, self).__init__(**kwargs)

        self.font = font
        self.text_color = text_color
        self._text = self.name
        self._text_rect = None

    @property
    def text(self):
        self._text = self.font.render(self.name, True, self.text_color)
        return self._text

    @property
    def text_rect(self):
        self._text_rect = self.text.get_rect()
        self._text_rect.center = self.pos
        return self._text_rect