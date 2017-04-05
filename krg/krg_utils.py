"""
================================== Helping utilities ==================================
"""


def in_circle(center, radius, mouse_pos):
    """
    :param center: center of the circle
    :param radius: krg of the circle
    :param mouse_pos: position of the mouse in a tuple (x, y)
    :return: boolean if the mouse is inside a given circle
    """
    center_x, center_y = center[0], center[1]
    x, y = mouse_pos[0], mouse_pos[1]
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2



