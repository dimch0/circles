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

    def set_body_room(self, grid, mybody):
        exit_button = Button()
        exit_button.name = "exit"
        exit_button.pos = grid.center_tile
        exit_button.img = mybody.img
        exit_button.available = True
        self.circles.append(exit_button)
        if not self in grid.rooms.keys():
            grid.rooms[self.name] = self

    def enter(self, grid):
        """ Shows the map room body_room """
        if not grid.current_room == self.name:
            grid.previous_room = grid.current_room
            grid.change_room(self.name)
            # grid.gen_map_dots()
            # grid.draw_map = True
        else:
            grid.change_room(grid.previous_room)
            # grid.draw_map = False