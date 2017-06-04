#######################################################################################################################
#################                                                                                     #################
#################                                 Button class                                        #################
#################                                                                                     #################
#######################################################################################################################
import math
from cir_item import Item
from math import sqrt, ceil, hypot


class ButtonItem(Item):
    """
    This is the base class for all circle items
    """
    # TODO: Move item options here?
    def __init__(self, font, text_color, text=None, **kwargs):
        super(ButtonItem, self).__init__(**kwargs)

        self.font = font
        self.text_color = text_color

        if text:
            self.text = self.font.render(text, True, self.text_color)
        else:
            self.text = self.font.render(self.name, True, self.text_color)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.pos
