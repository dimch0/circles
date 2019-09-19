from circle_button import Button


class Room(object):

    def __init__(self):
        self.room_name = None
        self.circles = []
        self.revealed_tiles = {}

class BodyRoom(Room):

    def __init__(self):
        super(BodyRoom, self).__init__()
        self.name = "body_room"

        exit_button = Button()
        exit_button.name = "exit"
