from circle import Circle


class Button(Circle):
    """
    A class for all circles that move
    """
    def __init__(self):
        super(Button, self).__init__()
        self.type = "button"
