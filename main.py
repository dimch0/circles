#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                                 Main file                                           #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################

# --------------------------------------------------------------- #
#                            FEATURES                             #
# --------------------------------------------------------------- #
# TODO: Time modifier
# TODO: Item generation on radar
# TODO: Create a mini map
# TODO: Define a signal function
# TODO: Log statistics during a lifespan
# TODO: Create spirit mode, calculate karma
# TODO: Log messages on screen
# TODO: Create save button
# TODO: Add sys argv for loading a game
# TODO: Animate instructions
# TODO: Animate item generation
# TODO: Animate activation of abilities
# TODO: Create installation .exe file
# --------------------------------------------------------------- #
#                            BUG FIXES                            #
# --------------------------------------------------------------- #
# TODO: Fix movement track
# --------------------------------------------------------------- #
#                            OPTIONAL                             #
# --------------------------------------------------------------- #
# TODO: Remove grid.bodies usage
# TODO: Remove mode_vs_options usage
# TODO: Link timer to body

import pdb

import os
import sys
import time
import pygame

from cir import cir_item
from cir import cir_grid
from cir import cir_draw
from cir import cir_utils
from cir import cir_loader
from cir import cir_cosmetic


def loading_general_settings():
    """
    Loading general game instances and settings
    :return: grid, images, fonts, clock
    """
    # Pygame
    pygame.init()

    # Grid
    grid = cir_grid.Grid()
    grid.game_display = pygame.display.set_mode((grid.display_width, grid.display_height))

    # Images and fonts
    images = cir_cosmetic.Images(grid, pygame)
    fonts = cir_cosmetic.Fonts(grid, pygame)

    # Settings
    pygame.display.set_caption(grid.caption)

    # pygame.mouse.set_visible(True)
    clock = pygame.time.Clock()

    return grid, images, fonts, clock


def load_items():
    """
    Loading all grid items, my body and mode options
    :return: my_body, mode_vs_options
    """
    my_body = None
    mode_vs_options = {}
    for item in cir_loader.load_data(grid, images, fonts, SCENARIO):
        category = item['category']
        item_obj = item['object']
        type = item["type"]
        if type == "mode_option":
            cir_loader.add_optoin_to_mode(category, item_obj, mode_vs_options)
        else:
            if category == "my body":
                my_body = cir_loader.set_grid_items(grid, item)
            else:
                cir_loader.set_grid_items(grid, item)

    cir_loader.set_item_mode_options(grid, mode_vs_options)

    return my_body, mode_vs_options


def game_loop():
    """ Main game loop. """

    print "Game started"

    GAME_EXIT = False
    START_TIME = time.time()
    # grid.game_menu = True




    while not GAME_EXIT:
        # Mouse
        MOUSE_POS = pygame.mouse.get_pos()
        # Seconds in game
        cir_utils.seconds_in_game(grid, START_TIME)

        # --------------------------------------------------------------- #
        #                                                                 #
        #                            EVENTS                               #
        #                                                                 #
        # --------------------------------------------------------------- #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GAME_EXIT = True

            # --------------------------------------------------------------- #
            #                           KEY EVENTS                            #
            # --------------------------------------------------------------- #
            elif event.type == pygame.KEYDOWN:

                # --------------------------------------------------------------- #
                #                            ESC KEY                              #
                # --------------------------------------------------------------- #
                if event.key == pygame.K_ESCAPE:
                    if not grid.game_menu:
                        grid.game_menu = True
                    elif grid.game_menu and grid.seconds_in_game > 0:
                        grid.game_menu = False

                # --------------------------------------------------------------- #
                #                            IN GAME                              #
                # --------------------------------------------------------------- #
                if not grid.game_menu:
                    # --------------------------------------------------------------- #
                    #                           SPACE KEY                             #
                    # --------------------------------------------------------------- #
                    if event.key == pygame.K_SPACE:

                        # RADAR Population
                        if not my_body.move_track and not my_body.in_menu and not my_body.radar_track:
                            my_body.gen_radar_track(grid)

                        # Debug
                        cir_utils.debug_print_space(grid)


                    # --------------------------------------------------------------- #
                    #                            't' KEY                              #
                    # --------------------------------------------------------------- #
                    elif event.key == pygame.K_t:
                            # Timers
                            if grid.timers:
                                for timer in grid.timers:
                                    if timer.name == "lifespan":
                                        print "step            :", timer.step
                                        print "filled_steps    :", timer.filled_steps
                                        print "number of steps :", timer.number_of_steps
                                        print "len of step     :", timer.len_step
                                        print "-"*20
                                        timer.step -= 200
                                        timer.filled_steps += 90

                    # --------------------------------------------------------------- #
                    #                            'l' KEY                              #
                    # --------------------------------------------------------------- #
                    elif event.key == pygame.K_l:
                        grid.game_over = True
                        sys.argv.append('Scenario_2')
                        os.execv(sys.executable, [sys.executable] + sys.argv)
                        print "l"

                    # --------------------------------------------------------------- #
                    #                            'r' KEY                              #
                    # --------------------------------------------------------------- #
                    elif event.key == pygame.K_r:
                        my_body.img = images.galab1
                        my_body.default_img = my_body.img
                        print "r"

                    # --------------------------------------------------------------- #
                    #                            'k' KEY                              #
                    # --------------------------------------------------------------- #
                    elif event.key == pygame.K_k:
                        for timer in grid.timers:
                            if timer.name == "lifespan":
                                pass
                        print "k"


                    # MOVEMENT Population
                    if not my_body.in_menu:
                        my_body.gen_movement_arrows(pygame, grid, event)

            # --------------------------------------------------------------- #
            #                           CLICK EVENTS                          #
            # --------------------------------------------------------------- #
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_circle = grid.mouse_in_tile(MOUSE_POS)
                if clicked_circle:


                    if grid.mouse_mode == "laino":
                        if clicked_circle not in grid.occupado_tiles:
                            hui = cir_item.Item(
                                name="hui",
                                color = grid.gelb,
                                image=images.laino3,
                                pos=clicked_circle,
                            )
                            if hui not in grid.items:
                                grid.items.append(hui)

                    # --------------------------------------------------------------- #
                    #                        CLICK IN GAME MENU                       #
                    # --------------------------------------------------------------- #
                    if grid.game_menu:
                        for button in grid.buttons:
                            if clicked_circle == button.pos and button.available:

                                if button.name in ["play", "replay"]:
                                    grid.game_menu = False
                                    if grid.game_over:
                                        grid.game_over = False

                                elif button.name == "quit":
                                    pygame.quit()
                                    quit()

                    # --------------------------------------------------------------- #
                    #                        CLICK GRID ITEMS                         #
                    # --------------------------------------------------------------- #
                    elif not grid.game_menu:
                        for item in grid.items:
                            if clicked_circle == item.pos and item.available:
                                # Set in_menu for the items with menu (my_body)
                                item.check_in_menu(grid, clicked_circle, mode_vs_options)
                                # Setting option positions
                                item.set_option_pos(grid)
                                # Option clicked
                                if item.in_menu:
                                    # Mouse mode image
                                    grid.mouse_mode = None
                                    grid.mouse_img = None

                            # --------------------------------------------------------------- #
                            #                       CLICK ITEM OPTIONS                        #
                            # --------------------------------------------------------------- #
                            elif clicked_circle in grid.adj_tiles(item.pos) and item.in_menu:
                                if item.options:
                                    for option in item.options:
                                        if clicked_circle == option.pos:
                                            # --------------------------------------------------------------- #
                                            #                       CLICK DEFAULT OPTIONS                     #
                                            # --------------------------------------------------------------- #
                                            if option in item.default_options:

                                                if option.name == "bag":
                                                    print "Gimme the loot!"

                                                if option.name == "mitosis":
                                                    item.mitosis(grid)

                                                # Setting the mode
                                                item.set_mode(grid, option, mode_vs_options)

                                            # --------------------------------------------------------------- #
                                            #                        CLICK SUB-OPTIONS                        #
                                            # --------------------------------------------------------------- #
                                            elif option in mode_vs_options[item.mode]:

                                                if item.mode == "move":
                                                    item.gen_move_track(grid, mode_vs_options[item.mode].index(option))

                                                elif option.name == "see":
                                                    item.range += 1
                                                    # item.mode = "seen"

                                                elif option.name == "smel":
                                                    print "sniff hair"

                                                elif option.name == "medi":
                                                    item.range += 3

                                                elif option.name == "audio":
                                                    item.change_speed(10)

                                                elif option.name == "eat":
                                                    item.change_speed(-1)

                                                # Close menu if option selected
                                                item.set_in_menu(grid, False)
                                            # Close menu if option has no suboptions
                                            if option.name not in mode_vs_options.keys():
                                                item.set_in_menu(grid, False)

                                            # --------------------------------------------------------------- #
                                            #                            MOUSE MODE                           #
                                            # --------------------------------------------------------------- #
                                            if option.modable:
                                                grid.mouse_mode = option.name
                                                if option.img and option.modable:
                                                    grid.mouse_img = option.img
                # Debug print
                cir_utils.debug_print_click(grid, MOUSE_POS, clicked_circle, my_body)

        # --------------------------------------------------------------- #
        #                                                                 #
        #                             DRAWING                             #
        #                                                                 #
        # --------------------------------------------------------------- #
        # BACKGROUND
        grid.game_display.fill(grid.dark_grey)
        # --------------------------------------------------------------- #
        #                             IN GAME                             #
        # --------------------------------------------------------------- #
        if not grid.game_menu:
            # Revealed radius
            if grid.revealed_radius:
                cir_draw.draw_revealed_radius(pygame, grid)

            # Mask
            cir_draw.draw_mask(pygame, grid)

            # Grid
            if grid.show_grid:
                cir_draw.draw_grid(pygame, grid)

            # Playing board:
            if grid.show_playing_tiles:
                cir_draw.draw_playing_tiles(pygame, grid)

            # --------------------------------------------------------------- #
            #                             ANIMATIONS                          #
            # --------------------------------------------------------------- #
            for item in grid.items:
                if item.available:

                    # Radar
                    if item.radar_track:
                        cir_draw.draw_radar(pygame, grid, item)

                    # Bodies
                    if (item.pos in grid.revealed_tiles) or (item in grid.bodies):
                        cir_draw.draw_body(pygame, grid, MOUSE_POS, item)

                    # Item options
                    if item.in_menu:
                        cir_draw.draw_item_options(pygame, grid, MOUSE_POS, item)


                    # Show movement track in color
                    if grid.show_movement and len(item.move_track) > 1:
                        cir_draw.draw_movement(pygame, grid, item)

                    # Image rotation
                    if item.rot_track:
                        item.rotate(pygame)

                    # Item reverse rotation
                    if item.last_direction and not item.move_track:
                        item.rotate_reverse(pygame)

            # Timers
            if grid.timers:
                cir_draw.draw_timers(pygame, grid, my_body)

        # --------------------------------------------------------------- #
        #                           GAME MENU                             #
        # --------------------------------------------------------------- #
        elif grid.game_menu:
            # Menu Buttons
            if grid.buttons:
                cir_draw.draw_menu_buttons(pygame, grid, MOUSE_POS)

        # Mouse
        # pygame.draw.CIR(grid.game_display, grid.white, MOUSE_POS, 2, 0)
        if grid.mouse_mode:
            cir_draw.draw_mouse_image(pygame, grid, MOUSE_POS)


        # === END DRAWING === #
        pygame.display.update()

        # --------------------------------------------------------------- #
        #                                                                 #
        #                           CHANGE VARS                           #
        #                                                                 #
        # --------------------------------------------------------------- #
        if not grid.game_menu:

            # Lifespan timer
            if grid.timers:

                for timer in grid.timers:
                    timer.tick()
                    if timer.name == "lifespan":
                        timer.pos = my_body.pos

            for item in grid.items:

                # Overlap
                item.overlapping(grid)

                # Movement
                if item.move_track:
                    item.move()

                # Clean placeholders
                grid.clean_placeholders(item)

            # Timers
            if grid.timers:
                for timer in grid.timers:
                    if timer.is_over:
                        # Lifespan
                        if timer.name == "lifespan":
                            grid.game_over = True
                            sys.argv.append('replay')
                            os.execv(sys.executable, [sys.executable] + sys.argv)

        # FPS
        clock.tick(grid.fps)

    #### END ####
    pygame.quit()
    quit()

# --------------------------------------------------------------- #
#                                                                 #
#                              MAIN                               #
#                                                                 #
# --------------------------------------------------------------- #
if __name__ == '__main__':

    # SCENARIO
    SCENARIO = cir_utils.set_scenario(sys.argv)

    # LOADING
    grid, images, fonts, clock = loading_general_settings()
    my_body, mode_vs_options = load_items()

    # REPLAY BUTTON
    for button in grid.buttons:
        if 'replay' not in sys.argv:
            if button.name == "replay":
                button.available = False
        else:
            if button.name == "replay":
                button.available = True
            if button.name == "play":
                button.available = False

    # GRID SETTINGS
    if 'Scenario_2' in sys.argv:
        grid.game_menu = False
    else:
        grid.game_menu = True

    # START
    game_loop()
