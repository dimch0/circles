#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                                 Helping Utilities                                   #################
#################                                                                                     #################
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
    if not grid.game_menu:
        if time.time() + grid.seconds_in_pause > (START_TIME + grid.seconds_in_game) - grid.seconds_in_pause:
            # print "second: {0}".format(grid.seconds_in_game)
            grid.seconds_in_game += 1


def debug_print_click(grid, MOUSE_POS, clicked_circle, my_body):
    """  Debug print on click event  """
    if grid.show_debug:
            print(""">>>>>> click: {0}, tile: {1}
        mouse mode  : {10}
        my_body mode: {2}
        menu        : {3}
        grid items  : {4}
        occupado:   : {5}
        playing     : {6}
        move track  : {7}
        all tiles   : {8}
        speed       : {9}
        """.format(MOUSE_POS,
                   clicked_circle,
                   my_body.mode,
                   my_body.in_menu,
                   [(item.name, item.pos) for item in grid.items],
                   [ot for ot in grid.occupado_tiles],
                   # len(grid._occupado_tiles),
                   len(grid.playing_tiles),
                   my_body.move_track,
                   len(grid.tiles),
                   my_body.speed,
                   grid.mouse_mode
                   )
                  )

def debug_print_space(grid):
    """  Debug print on space bar event  """
    if grid.show_debug:
        print(""">>>> space
    revealed tiles: {0}
    revealed_radius: {1}
    """.format(len(grid.revealed_tiles),
               len(grid.revealed_radius),
              )
             )

def negative_list(original_list):
    """ Returns the negative values of a list """
    return [-x for x in original_list]


def rot_center(pygame, image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def set_scenario(SYS_ARGV):
    """ Setting the scenario """
    result = "Scenario_1"
    for argument in SYS_ARGV:
        if "Scenario" in argument:
            result = argument
    return result

def set_argv(grid, argv):
    if 'Game Over' in argv:
        grid.everything["play"].available = False
        grid.everything["replay"].available = True
    if 'Scenario_2' in argv:
        grid.game_menu = False