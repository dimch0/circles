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

# IMAMGE LOADER
def imgLoader(imagefile):
    return pygame.image.load("img/"+imagefile)

feet_img = imgLoader('./feet.png')





my_body.default_options = [
    cir_item.Item(name="option 1", color=my_body.default_color),
    cir_item.Item(name="option 2", color=my_body.default_color),
    cir_item.Item(name="option 3", color=my_body.default_color),
    cir_item.Item(name="move", color=my_body.default_color),
    cir_item.Item(name="option 5", color=my_body.default_color),
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
move_option.img = feet_img
move_option.img = pygame.transform.scale(move_option.img, (grid.tile_radius, grid.tile_radius))

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
                        print "revealed radius: {0}".format(grid.revealed_radius)
                        print "REVEALED LEN: {0}".format(len(grid.revealed_radius))
            # -------------------------------------- SPACEBAR EVENTS -------------------------------------- #


            # -------------------------------------- CLICK EVENTS ----------------------------------------- #
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_circle = grid.mouse_in_tile(mouse_pos)
                if clicked_circle:
                    for item in grid.items:

                        # Movement track
                        if item.mode is "move" and not item.in_menu and not item.radar_track:
                            item.gen_move_track(clicked_circle, grid)

                        # If body is clicked check for menu
                        if item is my_body:
                            if clicked_circle == item.pos:
                                if item.in_menu == False:
                                    item.in_menu = True
                                elif item.in_menu and item.mode is item.name:
                                    item.in_menu = False
                                # Resetting the mode and options
                                elif item.mode is not item.name and item.in_menu:
                                    item.mode = item.name
                                    item.options = item.default_options
                                    item.color = item.default_color
                            elif clicked_circle is not item.pos and clicked_circle not in item.adj_tiles(grid):
                                item.in_menu = False

                        # If option is clicked
                        # Setting menu items position
                        item.set_option_pos(grid)
                        for option in item.options:
                            if item.in_menu:
                                if clicked_circle == option.pos:

                                    if option.name is "move":
                                        item.mode = option.name
                                        item.color = option.color
                                        item.options = option.default_options
                                        item.set_option_pos(grid)
                                    # Check for move options
                                    elif option in move_option.default_options:
                                        item.in_menu = False

                                    elif option.name is "sensory":
                                        item.mode = option.name
                                        item.color = option.color
                                        item.options = option.default_options
                                        item.set_option_pos(grid)
                                    # Check for sensory options
                                    elif option in sense_option.default_options:
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
            # TODO: place menu background
            if item.in_menu:
                for item_option in item.options:
                    pygame.draw.circle(gameDisplay, item_option.color, item_option.pos, grid.tile_radius, 0)
                    if item_option.img:
                        gameDisplay.blit(item_option.img,
                                         (item_option.pos[0] - grid.tile_radius / 2, item_option.pos[1] - grid.tile_radius / 2))

            # Body
            pygame.draw.circle(gameDisplay, item.color, item.pos, grid.tile_radius, 0)

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
