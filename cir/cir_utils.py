#######################################################################################################################
#################                                                                                     #################
#################                                 Helping Utilities                                   #################
#################                                                                                     #################
#######################################################################################################################



def in_circle(center, radius, point):
    """
    :param center: center of the circle
    :param radius: radius of the circle
    :param point: coordinates of the point to be checked (x, y)
    :return: boolean - is the point inside the given circle
    """
    center_x, center_y = center[0], center[1]
    x, y = point[0], point[1]
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2



