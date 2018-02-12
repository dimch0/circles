# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                   BUTTON                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
from cir_circle import Circle


class Button(Circle):
    """
    This is the base class for all Buttons
    """
    def __init__(self):
        super(Button, self).__init__()
        self.available = True
        self.font = None
        self.text_color = None
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