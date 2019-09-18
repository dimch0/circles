from circle import Circle
import random


class Door(Circle):
    """
    A class for all circles that move
    """
    def __init__(self):
        super(Door, self).__init__()
        self.side_1 = None
        self.side_2 = None

    def connect(self, grid):
        current_room_pos = grid.names_to_pos(grid.current_room)
        adj_rooms = grid.adj_tiles(current_room_pos)
        adj_rooms = [grid.pos_to_name(adj_pos) for adj_pos in adj_rooms]
        free_rooms = list(set(adj_rooms) - set(grid.rooms.keys()))
        random_adj_room = free_rooms[random.randrange(len(free_rooms))]
        self.side_1 = grid.current_room
        self.side_2 = random_adj_room


