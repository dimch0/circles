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

from cir import cir_body, cir_grid, cir_item, cir_utils, cir_img
pygame.init()







# Loading grid
grid = cir_grid.Grid()

# Loading images
images = cir_img.Images(grid)

# Creating bodies
my_body = cir_body.BodyItem(name="my body", color=grid.pink, speed=1)
my_body.pos = grid.center_tile
grid.items.append(my_body)

# Creating bokluk
if 1:
    bokluk = cir_body.MobileItem(name="bokluk", color=grid.green, speed = 0)
    # bokluk.pos = (my_body.pos[0], my_body.pos[1] - 2 * grid.tile_radius)
    bokluk.pos = (79, 140)
    grid.items.append(bokluk)


# TODO: Create MenuItem class
# TODO: Set menu item attr position in menu
# TODO: Generate items from external file
mode_vs_options = {
    "my body": [
        cir_item.Item(name="option 1", color=my_body.default_color),
        cir_item.Item(name="option 2", color=my_body.default_color),
        cir_item.Item(name="option 3", color=my_body.default_color),
        cir_item.Item(name="move", color=my_body.default_color, image=images.feet),
        cir_item.Item(name="option 5", color=my_body.default_color),
        cir_item.Item(name="sensory", color=grid.azure, image=images.brain),
    ],
    "move" : [
        cir_item.Item(name="North", color=grid.white, border=2),
        cir_item.Item(name="Northeast", color=grid.white, border=2),
        cir_item.Item(name="Southeast", color=grid.white, border=2),
        cir_item.Item(name="South", color=grid.white, border=2),
        cir_item.Item(name="Southwest", color=grid.white, border=2),
        cir_item.Item(name="Northwest", color=grid.white, border=2)
    ],
    "sensory": [
        cir_item.Item(name="eat", color=grid.azure, image=images.lips_y),
        cir_item.Item(name="audio", color=grid.azure, image=images.ear_y),
        cir_item.Item(name="smel", color=grid.azure, image=images.nose_y),
        cir_item.Item(name="medi", color=grid.azure, image=images.yoga),
        cir_item.Item(name="touch", color=grid.azure, image=images.touch_y),
        cir_item.Item(name="see", color=grid.azure, image=images.eye_y)
    ]
}

# Setting default options
for item in grid.items:
    for mode_name, mode_options in mode_vs_options.items():
        if item.name is mode_name:
            item.default_options = mode_options
            item.options = item.default_options



# GAME SETTINGS
gameDisplay = pygame.display.set_mode((grid.display_width, grid.display_height))
pygame.display.set_caption(grid.caption)
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)


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
                        print "revealed radius: {0}".format(grid.revealed_radius)
                        print "REVEALED LEN: {0}".format(len(grid.revealed_radius))
            # -------------------------------------- SPACEBAR EVENTS -------------------------------------- #


            # -------------------------------------- CLICK EVENTS ----------------------------------------- #
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_circle = grid.mouse_in_tile(mouse_pos)
                if clicked_circle:
                    for item in grid.items:

                        # Movement track
                        # if item.mode is "move" and not item.in_menu and not item.radar_track:
                        #     item.simple_move_track(clicked_circle, grid)

                        # =============================================================================================
                        # =============================================================================================
                        # TODO: parametrized function
                        # If body is clicked check for menu
                        if item is my_body:
                            # Clicked on item
                            if clicked_circle == item.pos:
                                # If default mode:
                                if item.mode is item.name:
                                    if not item.in_menu:
                                        item.in_menu = True
                                    elif item.in_menu:
                                        item.in_menu = False
                                # If not default - reset
                                elif item.mode is not item.name:
                                    if item.in_menu:
                                        item.reset_mode()
                                    elif not item.in_menu:
                                        item.in_menu = True
                            # Clicked outside
                            elif clicked_circle is not item.pos and clicked_circle not in item.adj_tiles(grid):
                                item.in_menu = False
                        # Setting option position
                        item.set_option_pos(grid)

                        # CLICKED ON MENU OPTION
                        if item.in_menu:
                            if item.options:
                                for option in item.options:
                                    if clicked_circle == option.pos:

                                        # If a default option -> set mode
                                        if option in item.default_options:
                                            item.set_mode(option, grid, mode_vs_options)

                                        # Check option specifics
                                        elif option in mode_vs_options[item.mode]:
                                            # TODO: make directions appear next to body when hovered
                                            # TODO: moving south:
                                            if option.name is "South":
                                                end_point = item.move_south(grid)[-1]
                                                # Movement track
                                                if item.mode is "move" and not item.radar_track:
                                                    print "here"
                                                    print "end_point", end_point
                                                    print item.simple_move_track(end_point, grid)


                                            # Check option "see"
                                            elif option.name is "see":
                                                item.range += 1
                                                # item.mode = "seen"
                                            # Close menu if option selected
                                            item.in_menu = False
                        # =============================================================================================
                        # =============================================================================================

                debug_print(mouse_pos, clicked_circle)
            # ------------------------------------- CLICK EVENTS ----------------------------------------- #

        # -------------------------------------- PLACEMENT --------------------------------------- #

        # -------------------------------------- Background -------------------------------------- #
        # Background
        gameDisplay.fill(grid.grey)

        # Revealed radius
        for revealed in grid.revealed_radius:
            pygame.draw.circle(gameDisplay, grid.ungrey, revealed[0], revealed[1], 0)
            printed = revealed
            if printed:
                for to_be_printed in grid.revealed_radius:
                    if printed[0] == to_be_printed[0]:
                        if printed[1] < to_be_printed[1]:
                            grid.revealed_radius.remove(printed)

        # Grid
        if grid.show_grid:
            for tile in grid.tiles:
                pygame.draw.circle(gameDisplay, grid.white, tile, grid.tile_radius, 1)
        # -------------------------------------- Background -------------------------------------- #


        # -------------------------------------- Animations -------------------------------------- #
        for item in grid.items:
            # Movement
            if item.move_track:
                item.move()

            # Radar
            if item.radar_track:
                radar_radius, thick = item.radar(grid)
                if radar_radius and thick:
                    pygame.draw.circle(gameDisplay, grid.green, item.pos, radar_radius, thick)

            # Item options
            if item.in_menu:
                # TODO: place menu background
                pygame.draw.circle(gameDisplay, item.color, item.pos, grid.tile_radius * 3, 0)
                for item_option in item.options:
                    pygame.draw.circle(gameDisplay, item_option.color, item_option.pos, grid.tile_radius, item_option.border)
                    if item_option.img:
                        gameDisplay.blit(item_option.img, item_option.set_img_pos(grid))

            # Body
            pygame.draw.circle(gameDisplay, item.color, item.pos, grid.tile_radius, item.border)
            if item.img:
                gameDisplay.blit(item.img, item.set_img_pos(grid))

        # Mouse Item
        # TODO: Create MouseItem
        pygame.draw.circle(gameDisplay, grid.white, mouse_pos, 1, 0)
        pygame.draw.circle(gameDisplay, grid.black, mouse_pos, 2, 1)
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
