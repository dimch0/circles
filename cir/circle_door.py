import random

from circle import Circle
from grid_util import get_mirror_point, intersecting, get_short_name, in_circle



class Door(Circle):
    """
    A class for all circles that move
    """
    def __init__(self):
        super(Door, self).__init__()
        self.side_1 = None
        self.side_2 = None

        # Private
        self.adj_room = None

    def connect(self, grid):
        current_room_pos = grid.names_to_pos(grid.current_room)
        adj_rooms = grid.adj_tiles(current_room_pos)
        adj_rooms = [grid.pos_to_name(adj_pos) for adj_pos in adj_rooms]
        free_rooms = list(set(adj_rooms) - set(grid.rooms.keys()))
        self.adj_room = free_rooms[random.randrange(len(free_rooms))]
        self.side_1 = grid.current_room
        self.side_2 = self.adj_room

    def create_mirror_door(self, grid):
        # Create backwards door
        mirror_pos = get_mirror_point(self.pos, grid.center_tile)
        mirror_door = grid.event_effects.produce(self.name, mirror_pos)
        mirror_door.side_1 = self.side_2
        mirror_door.side_2 = self.side_1
        grid.should_change_room = False
