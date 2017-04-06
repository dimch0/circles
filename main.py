"""
================================== Main file ==================================
"""


import pygame
import time
import random
from pygame.locals import *

from krg import krg_body, krg_grid, krg_utils
pygame.init()


# COLORS
white = (255, 255, 255)
black = (0, 0, 0)
ungrey = (195, 195, 195)
grey = (175, 165, 175)
pink = (252, 217, 229)
green = (210, 255, 191)

# DEFAULT SCALE IS 1, INCREASE THE NUMBER FOR A SMALLER SIZE
SCALE = 4
FPS = 100
SPEED = 5
SHOW_GRID = False

# SETTINGS
circle_radius = 30 / SCALE
display_width = 600 / SCALE
display_height = 600 / SCALE
mid_x = int(display_width/2)
mid_y = int(display_height/2)
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('krg')
clock = pygame.time.Clock()


grid = krg_grid.Grid(circle_radius)
grid.tiles = grid.grid_gen(circle_radius)
player = krg_body.Body()
grid.items.append(player)



print "Player born."
print "Grid created."
print "Grid tiles:", grid.tiles.keys()
print "Number of tiles:", len(grid.tiles.keys())

def game_loop():
    """
    main game loop
    """
    print "INFO Game started"
    pygame.mouse.set_visible(1)
    game_exit = False
    player.pos = (mid_x, mid_y)
    menu = False
    radar = 0

    while not game_exit:
        # MOUSE POSITION X AND Y
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            # print event
            if event.type == pygame.QUIT:
                game_exit = True

            # CLICK EVENTS
            if event.type == pygame.MOUSEBUTTONDOWN:

                clicked_circle = krg_grid.Grid.mouse_in_tile(circle_radius, mouse_pos)

                print "-" * 30
                print "click:", mouse_pos
                print "circle:", clicked_circle

                radar = 0


                if clicked_circle:

                    # CHECK CLICKED ITEMS
                    for item in grid.items:
                        if clicked_circle == item.pos:
                            # item.menu(grid).
                            item.in_menu = True
                        else:
                            item.in_menu = False

                        for option in item.options:
                            if item.in_menu:
                                option.pos = (player.pos[0], player.pos[1] + circle_radius * 2)
                                grid.items.append(option)
                            elif not item.in_menu and option in grid.items:
                                grid.items.remove(option)

                    print "DEBUG items", grid.items



                    # MOVEMENT populating tracks
                    track = player.tracks(clicked_circle)
                    print "track:", track
                if krg_utils.in_circle(player.pos, circle_radius, mouse_pos) and not menu:
                    menu = True
                else:
                    menu = False

        # MOVEMENT only moves if tracks are populated
        player.move()

        # BLIT BACKGROUND
        gameDisplay.fill(grey)
        # BLIT UNGREY
        for rgrid in grid.revealed_radius:
            pygame.draw.circle(gameDisplay, ungrey, rgrid[0], rgrid[1], 0)

        # TODO blit stuff here

        if SHOW_GRID:
            for tile in grid.tiles.values():
                pygame.draw.circle(gameDisplay, white, tile, circle_radius, 1)

        # MENU / RADAR
        if menu:
            # pygame.draw.circle(gameDisplay, green, player.pos, circle_radius * 3, 0)
            pass

            # # RADAR
            # limit = circle_radius * 2
            # thikness = range(1, circle_radius)
            # thikness.reverse()
            # if radar < limit:
            #     for thik in thikness:
            #         if radar < limit / thik:
            #             pygame.draw.circle(gameDisplay, green, player.pos, circle_radius + radar, thik)
            #     radar += 1
            #     # FILL TERRITORY UNGREY
            #     if radar == limit:
            #         grid.revealed_radius.append((player.pos, (circle_radius + radar)))
            # # ongoing radar
            # # else:
            # #     radar = 0

        # BLIT BODY / ITEMS
        for item in grid.items:
            pygame.draw.circle(gameDisplay, pink, item.pos, circle_radius, 0)

        # MOUSE IMG
        for tile in grid.tiles.values():
            if krg_utils.in_circle(tile, circle_radius, mouse_pos):
                pygame.draw.circle(gameDisplay, white, tile, circle_radius, 1)

        # UPDATE DISPLAY
        pygame.display.update()

        # TODO: if change vars to blit

        clock.tick(FPS)
    pygame.quit()
    quit()


if __name__ == '__main__':
    game_loop()
