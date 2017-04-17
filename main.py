#######################################################################################################################
#################                                                                                     #################
#################                                 Main file                                           #################
#################                                                                                     #################
#######################################################################################################################
import pdb
import pygame
# import time
# import random
from pygame.locals import *

from cir import cir_body, cir_grid, cir_item, cir_utils
pygame.init()


# Creating grid
grid = cir_grid.Grid()

# Creating player
my_body = cir_body.BodyItem(name="my body", color=grid.pink, speed=4)
my_body.pos = grid.center_tile
# TODO: Create MenuItem class
# TODO: Define body to assign options

my_body.default_options = [
    cir_item.Item(name="option 1", color=grid.gelb),
    cir_item.Item(name="option 2", color=grid.gelb),
    cir_item.Item(name="option 3", color=grid.gelb),
    cir_item.Item(name="move", color=grid.white),
    cir_item.Item(name="option 5", color=grid.gelb),
    cir_item.Item(name="sensory", color=grid.azure),
]
move_options = [
    cir_item.Item(name="direction 1", color=grid.white),
    cir_item.Item(name="direction 2", color=grid.white),
    cir_item.Item(name="direction 3", color=grid.white),
    cir_item.Item(name="direction 4", color=grid.white),
    cir_item.Item(name="direction 5", color=grid.white),
    cir_item.Item(name="direction 6", color=grid.white)
]
sense_options = [
    cir_item.Item(name="eat", color=grid.blue),
    cir_item.Item(name="audio", color=grid.blue),
    cir_item.Item(name="smel", color=grid.blue),
    cir_item.Item(name="touch", color=grid.blue),
    cir_item.Item(name="see", color=grid.blue),
    cir_item.Item(name="medi", color=grid.blue)
]

move_option = [option for option in my_body.default_options if option.name is "move"][0]
move_option.default_options = move_options

sense_option = [option for option in my_body.default_options if option.name is "sensory"][0]
sense_option.default_options = sense_options

# Creating my body
my_body.options = my_body.default_options
grid.items.append(my_body)

# Creating bokluk
bokluk = cir_body.MobileItem(name="bokluk", color=grid.green, speed = 0)
bokluk.pos = (my_body.pos[0], my_body.pos[1] - 2 * grid.tile_radius)
grid.items.append(bokluk)

# GAME SETTINGS
gameDisplay = pygame.display.set_mode((grid.display_width, grid.display_height))
pygame.display.set_caption(grid.caption)
clock = pygame.time.Clock()
pygame.mouse.set_visible(1)


def debug_print(mouse_pos, clicked_circle):
    print(""">>>>>> click: {0}, tile: {1}
mode        : {2}
menu        : {3}
grid items  : {4}
""".format(mouse_pos,
           clicked_circle,
           my_body.mode,
           my_body.in_menu,
           [item.name for item in grid.items],
           grid.occupado_tiles
           )
          )


def game_loop():
    """
    The main game loop.
    """
    game_exit = False

    while not game_exit:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            # TODO: K_ESCAPE screen
            # -------------------------------------- SPACEBAR EVENTS -------------------------------------- #
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Radar track populating
                    if not my_body.move_track and not my_body.in_menu and not my_body.radar_track:
                        my_body.gen_radar_track(grid)
                        print ">>>> space"
                        print "revealed tiles: {0}".format(grid.revealed_tiles)
            # -------------------------------------- SPACEBAR EVENTS -------------------------------------- #


            # -------------------------------------- CLICK EVENTS ----------------------------------------- #
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_circle = grid.mouse_in_tile(mouse_pos)
                if clicked_circle:


                    # Movement track populating
                    if my_body.mode is "move" and not my_body.in_menu and not my_body.radar_track:
                        my_body.gen_move_track(clicked_circle, grid)


                    # Check for item menu
                    for item in grid.items:
                        # If body is clicked
                        if item is my_body:
                            if clicked_circle == item.pos:
                                if item.in_menu == False:
                                    print "TUKA STAVA TRUE"
                                    item.in_menu = True
                                elif item.in_menu and item.mode is item.name:
                                    item.in_menu = False
                                # Resetting the mode and options
                                elif item.mode is not item.name and item.in_menu:
                                    item.mode = item.name
                                    item.options = item.default_options
                            elif clicked_circle is not item.pos and clicked_circle not in item.adj_tiles(grid):
                                item.in_menu = False

                        # Setting menu items position
                        item.set_option_pos(grid)
                        # If option is clicked
                        for option in item.options:
                            print "ZASHTO SUM TUK?", item.in_menu
                            if item.in_menu:
                                if clicked_circle == option.pos:
                                    # Move opt
                                    if option.name is "move":
                                        item.mode = option.name
                                        item.options = option.default_options
                                        item.set_option_pos(grid)
                                    # Check for move options
                                    elif option in move_option.default_options:

                                        item.in_menu = False

                                    elif option.name is "sensory":
                                        item.mode = option.name
                                        item.options = option.default_options
                                        item.set_option_pos(grid)
                                    # Check for sensory options
                                    elif option in sense_option.default_options:
                                        print "Sensory option:", option.name
                                        item.in_menu = False


                debug_print(mouse_pos, clicked_circle)
            # ------------------------------------- CLICK EVENTS ----------------------------------------- #

        # -------------------------------------- PLACEMENT --------------------------------------- #

        # -------------------------------------- Background -------------------------------------- #
        # Background
        gameDisplay.fill(grid.grey)

        # Revealed radius
        for revealed in grid.revealed_radius:
            pygame.draw.circle(gameDisplay, grid.ungrey, revealed[0], revealed[1], 0)

        # TODO: place menu background

        # Grid
        if grid.show_grid:
            for tile in grid.tiles:
                pygame.draw.circle(gameDisplay, grid.white, tile, grid.tile_radius, 1)
        # -------------------------------------- Background -------------------------------------- #


        # -------------------------------------- Animations -------------------------------------- #
        # Radar
        if my_body.radar_track:
            radar_radius, thick = my_body.radar(grid)
            if radar_radius and thick:
                pygame.draw.circle(gameDisplay, grid.green, my_body.pos, radar_radius, thick)

        # Movement
        if my_body.move_track:
            my_body.move()

        # Items and Body
        for item in grid.items:
            # TODO: check color for mode specifics
            if my_body.mode is "move":
                my_body.color = grid.white
            elif my_body.mode is "sensory":
                my_body.color = grid.azure
            else:
                my_body.color = grid.pink
            pygame.draw.circle(gameDisplay, item.color, item.pos, grid.tile_radius, 0)
            # Item options
            if item.in_menu:
                for item_option in item.options:
                    pygame.draw.circle(gameDisplay, item_option.color, item_option.pos, grid.tile_radius, 0)

        # Mouse image
        for tile in grid.tiles:
            if cir_utils.in_circle(tile, grid.tile_radius, mouse_pos):
                pygame.draw.circle(gameDisplay, grid.white, tile, grid.tile_radius, 1)
        # -------------------------------------- Animations -------------------------------------- #

        # -------------------------------------- PLACEMENT --------------------------------------- #

        pygame.display.update()
        # TODO: check changes for placement
        clock.tick(grid.fps)
    pygame.quit()
    quit()

if __name__ == '__main__':
    game_loop()
