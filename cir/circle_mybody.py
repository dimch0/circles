from circle_body import Body


class MyBody(Body):
    """
    This class holds all attributes and metrics of a body
    """
    def __init__(self):
        super(MyBody, self).__init__()
        self.body_room = None