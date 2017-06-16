#######################################################################################################################
#################                                                                                     #################
#################                                 Helping Utilities                                   #################
#################                                                                                     #################
#######################################################################################################################
import time


def in_circle(center, radius, point):
    """
    :param center: center of the CIR
    :param radius: radius of the CIR
    :param point: coordinates of the point to be checked (x, y)
    :return: boolean - is the point inside the given CIR
    """
    center_x, center_y = center[0], center[1]
    x, y = point[0], point[1]
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2


def inside_polygon(poly, point):
    """
    Return True if a coordinate (x, y) is inside a polygon defined by
    a list of verticies [(x1, y1), (x2, x2), ... , (xN, yN)].

    Reference: http://www.ariel.com.au/a/python-point-int-poly.html
    """
    x = point[0]
    y = point[1]

    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(1, n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def seconds_in_game(grid, START_TIME):
    """ Counts the seconds in the game """
    # TODO: FIX START TIME AND PAUSE SECONDS
    pass
    # if not grid.game_menu:
    #     if time.time() + grid.seconds_in_pause > (START_TIME + grid.seconds_in_game) - grid.seconds_in_pause:
    #         print "second: {0}".format(grid.seconds_in_game)
    #         grid.seconds_in_game += 1


def debug_print_click(grid, MOUSE_POS, clicked_circle, my_body):
    """  Debug print on click event  """
    print(""">>>>>> click: {0}, tile: {1}
mode        : {2}
menu        : {3}
grid items  : {4}
occupado:   : {5}
playing     : {6}
move track  : {7}
all tiles   : {8}
speed       : {9}
overlap     : {10}
""".format(MOUSE_POS,
           clicked_circle,
           my_body.mode,
           my_body.in_menu,
           len([item.name for item in grid.items]),
           len(grid.occupado_tiles),
           len(grid.playing_tiles),
           my_body.move_track,
           len(grid.tiles),
           my_body.speed,
           len(grid.overlap)
           )
          )


def debug_print_space(grid):
    """  Debug print on space bar event  """
    print(""">>>> space
revealed tiles: {0}
revealed_radius: {0}
""".format(len(grid.revealed_tiles),
           len(grid.revealed_radius),
          )
         )


def clean_placeholders(grid, item):
    if item.name == "placeholder":
        for other_item in grid.items:
            if other_item.pos == item.pos:
                grid.items.remove(item)