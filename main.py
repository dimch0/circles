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

move_option = cir_item.Item(name="move", color=grid.gelb)
menu_option_2 = cir_item.Item(name="option_2", color=grid.gelb)
menu_option_3 = cir_item.Item(name="option_3", color=grid.gelb)
radar_option = cir_item.Item(name="radar", color=grid.gelb)
menu_option_5 = cir_item.Item(name="option_5", color=grid.gelb)
menu_option_6 = cir_item.Item(name="option_6", color=grid.gelb)


my_body.options.append(move_option)
my_body.options.append(menu_option_2)
my_body.options.append(menu_option_3)
my_body.options.append(radar_option)
my_body.options.append(menu_option_5)
my_body.options.append(menu_option_6)


grid.items.append(my_body)

# Creating bokluk
# bokluk = cir_body.MobileItem(name="bokluk", color=grid.green, speed = 0)
# bokluk.pos = (591, 270)
# grid.items.append(bokluk)

# GAME SETTINGS
gameDisplay = pygame.display.set_mode((grid.display_width, grid.display_height))
pygame.display.set_caption(grid.caption)
clock = pygame.time.Clock()
pygame.mouse.set_visible(1)


def debug_print(mouse_pos, clicked_circle):
    print("""
>>>>>> click: {0}, tile: {1}
modes       : {2}
grid items  : {3}
occupado    : {4}
""".format(mouse_pos,
           clicked_circle,
           grid.mode,
           [item.name for item in grid.items],
           grid.occupado_tiles))


# grid.mode.append("move")
# grid.mode.append("radar")

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
            # Radar track populating
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print ">>>> space"
                    if "radar" in grid.mode:
                        my_body.gen_radar_track(grid)
                        print "revealed tiles: {0}".format(grid.revealed_tiles)
            # -------------------------------------- SPACEBAR EVENTS -------------------------------------- #


            # -------------------------------------- CLICK EVENTS ----------------------------------------- #
            if event.type == pygame.MOUSEBUTTONDOWN:

                clicked_circle = grid.mouse_in_tile(mouse_pos)
                if clicked_circle:

                    # Movement track populating
                    if "move" in grid.mode and not my_body.in_menu:
                        my_body.gen_move_track(clicked_circle, grid)



                    # Setting the mode
                    for item in grid.items:
                        if clicked_circle == item.pos:
                            print "ITEM_CLICKED:", item.name
                            if not item.name in grid.mode:
                                grid.mode.append(item.name)

                    # Check for item menu
                    for item in grid.items:
                        item.open_menu(clicked_circle, grid)

                debug_print(mouse_pos, clicked_circle)
            # ------------------------------------- CLICK EVENTS ----------------------------------------- #

        # -------------------------------------- BACKGROUND -------------------------------------- #
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
        # -------------------------------------- BACKGROUND -------------------------------------- #


        # -------------------------------------- ANIMATIONS -------------------------------------- #
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
            pygame.draw.circle(gameDisplay, item.color, item.pos, grid.tile_radius, 0)

        # Mouse image
        for tile in grid.tiles:
            if cir_utils.in_circle(tile, grid.tile_radius, mouse_pos):
                pygame.draw.circle(gameDisplay, grid.white, tile, grid.tile_radius, 1)
        # -------------------------------------- ANIMATIONS -------------------------------------- #


        pygame.display.update()
        # TODO: check changes for placement
        clock.tick(grid.fps)
    pygame.quit()
    quit()

if __name__ == '__main__':
    game_loop()
