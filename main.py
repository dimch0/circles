import pygame, random
from pygame.locals import *
import time
from math import sqrt
pygame.init()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
grey = (195, 195, 195)
pink = (252, 217, 229)
green = (210, 255, 191)

# DEFAUL SCALE IS 1, INCREASE THE NUMBER FOR A SMALLER SIZE
SCALE = 1
FPS = 30

circle_radius = 30 / SCALE
SPEED = 5
display_width = 600 / SCALE
display_height = 600 / SCALE
mid_x = int(display_width/2)
mid_y = int(display_height/2)
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('radius')
clock = pygame.time.Clock()


def in_circle(center, radius, mouse_pos):
    """
    :param center: center of the circle
    :param radius: radius of the circle
    :param mouse_pos: position of the mouse in a tuple (x, y)
    :return: boolean if the mouse is inside a given circle
    """
    center_x, center_y = center[0], center[1]
    x, y = mouse_pos[0], mouse_pos[1]
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2


class Grid(object):
    """
    master class for the grid
    """
    def __init__(self, circle_radius):
        self.tile_radius = circle_radius
        self.tiles = []
        self.occupado = []
        self.revealed = []

    @staticmethod
    def grid_gen(circle_radius):
        """
        :param circle_radius:
        :return:
        """
        result = {}
        katet = int(sqrt(((2 * circle_radius) ** 2) - (circle_radius ** 2)))
        for x in range(0, 12):
            for y in range(1, 20):
                if x % 2 == y % 2:
                    centre_x = circle_radius + (x * katet)
                    centre_y = y * circle_radius
                    centre = (centre_x, centre_y)
                    name = "{0}, {1}".format(x, y)
                    result[name] = centre
                    # pygame.draw.circle(gameDisplay, white, centre, circle_radius, 1)
        return result

    @staticmethod
    def mouse_in_circle(circle_radius, mouse_pos):
        current_circle = None
        grid = Grid.grid_gen(circle_radius)
        for circle in grid.values():
            if in_circle(circle, circle_radius, mouse_pos):
                current_circle = circle
        return current_circle



grid = Grid(circle_radius)
grid.tiles = grid.grid_gen(circle_radius)
print "Grid created:", grid


def Tracks(point_A, Point_B, speed = SPEED):
    """
    :param point_A: coordinates of point A (x, y)
    :param Point_B: coordinates of point B (x, y)
    :param speed: pixels moved for each step
    :return: a list of steps from point A to point B
    """
    track = []
    ax = point_A[0]
    ay = point_A[1]
    bx = Point_B[0]
    by = Point_B[1]
    dx, dy = (bx - ax, by - ay)
    distance = sqrt(dx**2 + dy**2)

    steps_number = int(distance / speed)
    if steps_number > 0:
        stepx, stepy = int(dx / steps_number), int(dy / steps_number)
        for i in range(steps_number+1):
            step = [int(ax + stepx * i), int(ay + stepy * i)]
            track.append(step)
    track.append(Point_B)
    return track


def game_loop():
    """
    main game loop
    """
    game_exit = False
    lead_x = mid_x
    lead_y = mid_y
    menu = False
    track = []
    radar = 0

    while not game_exit:
        # MOUSE POSITION X AND Y
        mouse_pos = pygame.mouse.get_pos()
        mx = mouse_pos[0]
        my = mouse_pos[1]

        for event in pygame.event.get():
            # print event
            if event.type == pygame.QUIT:
                game_exit = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                print "-" * 30
                print "click:", mouse_pos
                print "circle:", Grid.mouse_in_circle(circle_radius, mouse_pos)
                clicked_circle = Grid.mouse_in_circle(circle_radius, mouse_pos)
                if clicked_circle:
                    track = Tracks((lead_x, lead_y), clicked_circle)
                    print "track:", track

                if in_circle((lead_x, lead_y), circle_radius, mouse_pos) and not menu:
                    menu = True
                    print "menu:", menu
                else:
                    menu = False
                    print "menu:", menu

        # MOVEMENT
        if track:
            lead_x = track[0][0]
            lead_y = track[0][1]
            track.pop(0)

        # BACKGROUND
        gameDisplay.fill(grey)

        # TODO blit stuff here

        # GRID
        # for centre in grid.tiles.values():
        #     pygame.draw.circle(gameDisplay, white, centre, circle_radius, 1)

        # MENU
        if menu:
            # pygame.draw.circle(gameDisplay, green, [lead_x, lead_y], circle_radius * 3, 0)
            if radar < circle_radius * 3:
                pygame.draw.circle(gameDisplay, green, [lead_x, lead_y], circle_radius + radar, 1)
                radar += 1
            else:
                radar = 0

        # BODY
        pygame.draw.circle(gameDisplay, pink, (lead_x, lead_y), circle_radius, 0)

        # UPDATE DISPLAY
        pygame.display.update()

        # TODO: if change vars to blit

        clock.tick(FPS)

    pygame.quit()
    quit()


if __name__ == '__main__':
    game_loop()
