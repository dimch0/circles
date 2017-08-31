#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                                 Helping Utilities                                   #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
import math


def dist_between(pointA, pointB):
    x1 = pointA[0]
    y1 = pointA[1]
    x2 = pointB[0]
    y2 = pointB[1]

    return math.sqrt(((x2 - x1)*(x2 - x1)) + ((y2 - y1)*(y2 - y1)))

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


def intersecting(circle_1, circle_2):
    """
    Given two circles described by the 3-tuples (x-coordinates, y-coordinates, radius)
    :param circle_1: ((x1, y1), r1)
    :param circle_2: ((x1, y1), r1)
    :return: Boolean
    """
    x1 = circle_1[0][0]
    y1 = circle_1[0][1]
    r1 = circle_1[1] - 1
    x2 = circle_2[0][0]
    y2 = circle_2[0][1]
    r2 = circle_2[1] - 1
    return math.pow(abs(x1 - x2),2) + math.pow(abs(y1 - y2),2) < math.pow((r1 + r2),2)


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



def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step


def get_list_drange(start, stop, step):
    i0 = drange(start, stop, step)
    result = [x for x in i0]
    return result


def get_next_point(pointA, pointB, dist):

    x1 = pointA[0]
    y1 = pointA[1]
    x2 = pointB[0]
    y2 = pointB[1]

    new_x = x1 * (1 - dist) + x2 * dist
    new_y = y1 * (1 - dist) + y2 * dist
    new_step = (new_x, new_y)

    return new_step


def get_mirror_point(pointA, pointB):

    # print("INFO: Mirroring {0}".format(pointB))
    dist = 2
    t = 1
    pointC = get_next_point(pointA, pointB, dist)
    dx = int(((1 - t) * pointB[0]) + (t * pointC[0]))
    dy = int(((1 - t) * pointB[1]) + (t * pointC[1]))

    return (dx, dy)


def debug_print_click(grid, current_circle, my_body):
    """  Debug print on click event  """
    if grid.show_debug:
        print('')
        grid.logger.log(grid.logger.DEBUG, "click tile  : {0}".format( current_circle ))
        grid.logger.log(grid.logger.DEBUG, "mouse mode  : {0}".format( grid.mouse_mode ))
        grid.logger.log(grid.logger.DEBUG, "my_body mode: {0}".format( my_body.mode ))
        grid.logger.log(grid.logger.DEBUG, "menu        : {0}".format( my_body.in_menu ))
        grid.logger.log(grid.logger.DEBUG, "grid items  : {0}".format( len(grid.items) ))
        grid.logger.log(grid.logger.DEBUG, "grid items  : {0}".format( [(item.name, item.pos) for item in grid.items] ))
        grid.logger.log(grid.logger.DEBUG, "occupado    : {0}".format( len(grid.occupado_tiles) ))
        grid.logger.log(grid.logger.DEBUG, "overlap     : {0}".format( [(item.name, item.pos) for item in grid.overlap] ))
        grid.logger.log(grid.logger.DEBUG, "playing     : {0}".format( len(grid.playing_tiles) ))
        grid.logger.log(grid.logger.DEBUG, "move track  : {0}".format( my_body.move_track ))
        grid.logger.log(grid.logger.DEBUG, "all tiles   : {0}".format( len(grid.tiles) ))
        grid.logger.log(grid.logger.DEBUG, "current room: {0}".format( grid.current_room ))
        grid.logger.log(grid.logger.DEBUG, "prev room   : {0}".format( grid.previous_room ))
        grid.logger.log(grid.logger.DEBUG, "revealed    : {0}".format( grid.revealed_radius ))


def debug_print_space(grid, my_body):
    """  Debug print on space bar event  """
    if grid.show_debug:
        grid.logger.log(grid.logger.DEBUG, "Key SPACE pressed")
        grid.logger.log(grid.logger.DEBUG, "revealed tiles  : {0}".format( len(grid.revealed_tiles) ))
        grid.logger.log(grid.logger.DEBUG, "revealed_radius : {0}".format( len(grid.revealed_radius) ))
        grid.logger.log(grid.logger.DEBUG, "vibe speed      : {0}".format( my_body.vibe_speed ))


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