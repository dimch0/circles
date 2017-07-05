#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                                    Main file                                        #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
# --------------------------------------------------------------- #
#                            Features                             #
# --------------------------------------------------------------- #
# TODO: Time modifier
# TODO: Tile names
# TODO: Item generation
# TODO: Make game menu = room 0
# TODO: Indicate uses
# TODO: Create mini map
# TODO: Define signal function
# TODO: Log statistics during a lifespan
# TODO: Create spirit mode, calculate karma
# TODO: Log messages on screen
# TODO: Create / load button
# TODO: Create installation .exe file
# --------------------------------------------------------------- #
#                            Animation                            #
# --------------------------------------------------------------- #
# TODO: Animate item generation
# TODO: Animate item activation
# TODO: Animate menu opening
# TODO: Animate room transition
# TODO: Animate circle kiss
# TODO: Animate instructions
# --------------------------------------------------------------- #
#                            Bug fixes                            #
# --------------------------------------------------------------- #
# TODO: Fix movement track

import os
import sys
import time
import pygame
pygame.init()

from cir import cir_grid
from cir import cir_draw
from cir import cir_utils
from cir import cir_loader
from cir import cir_item_effects
from cir import cir_cosmetic



def game_loop():
    """ Main game loop """
    print "Game started"
    GAME_EXIT = False
    START_TIME = time.time()


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
            #                                                                 #
            #                            KEY EVENTS                           #
            #                                                                 #
            # --------------------------------------------------------------- #
            elif event.type == pygame.KEYDOWN:
                # --------------------------------------------------------------- #
                #                             'Esc'                               #
                # --------------------------------------------------------------- #
                if event.key == pygame.K_ESCAPE:
                    grid.current_room = 0
                    if not grid.game_menu:
                        grid.game_menu = True
                    elif grid.game_menu and grid.seconds_in_game > 0:
                        grid.game_menu = False
                # --------------------------------------------------------------- #
                #                            IN GAME                              #
                # --------------------------------------------------------------- #
                if not grid.game_menu:
                    # --------------------------------------------------------------- #
                    #                            'Space'                              #
                    # --------------------------------------------------------------- #
                    if event.key == pygame.K_SPACE:
                        # Radar Population
                        if not my_body.move_track and not my_body.in_menu and not my_body.radar_track:
                            my_body.gen_radar_track(grid)
                        # Debug
                        cir_utils.debug_print_space(grid)

                    elif event.key == pygame.K_t:
                            # Lifespan timer
                            lst = grid.everything["lifespan"]
                            print "step            :", lst.step
                            print "filled steps    :", lst.filled_steps
                            print "number of steps :", lst.number_of_steps
                            print "len of step     :", lst.len_step
                            print "-"*35
                            lst.step -= 20
                            lst.filled_steps += 20

                    elif event.key == pygame.K_l:
                        grid.game_over = True
                        sys.argv.append('Scenario_2')
                        os.execv(sys.executable, [sys.executable] + sys.argv)
                        print "l"

                    elif event.key == pygame.K_b:
                        grid.change_room(2)
                        print "b"

                    elif event.key == pygame.K_r:
                        grid.change_room(1)
                        print "r"

                    elif event.key == pygame.K_k:
                        my_body.img = images.galab
                        my_body.default_img = my_body.img
                        print "k"

                    # Movement Population
                    elif not my_body.in_menu:
                        my_body.gen_movement_arrows(pygame, grid, event)

            # --------------------------------------------------------------- #
            #                                                                 #
            #                          CLICK EVENTS                           #
            #                                                                 #
            # --------------------------------------------------------------- #
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_circle = grid.mouse_in_tile(MOUSE_POS)
                if clicked_circle:
                    # --------------------------------------------------------------- #
                    #                            GAME MENU                            #
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
                    else:
                        # --------------------------------------------------------------- #
                        #                        MOUSE MODES CLICK                        #
                        # --------------------------------------------------------------- #
                        if grid.mouse_mode == "laino":
                            cir_item_effects.laino_mode_click(grid, clicked_circle)
                        elif grid.mouse_mode == "shit":
                            cir_item_effects.shit_mode_click(grid, clicked_circle)

                        # --------------------------------------------------------------- #
                        #                          CLICK ON ITEMS                         #
                        # --------------------------------------------------------------- #
                        for item in grid.items:
                            if item.available:
                                if clicked_circle == item.pos:
                                    # --------------------------------------------------------------- #
                                    #                            BAG MODE                             #
                                    # --------------------------------------------------------------- #
                                    if grid.mouse_mode == "bag":
                                        cir_item_effects.collect(grid, item)

                                    # Set in_menu for the items with menu (my_body)
                                    item.check_in_menu(grid, clicked_circle)
                                    # Setting option positions
                                    item.set_option_pos(grid)
                                    # Option clicked
                                    if item.in_menu:
                                        grid.clean_mouse()
                                # --------------------------------------------------------------- #
                                #                       CLICK ITEM OPTIONS                        #
                                # --------------------------------------------------------------- #
                                elif clicked_circle in grid.adj_tiles(item.pos) and item.in_menu:
                                    if item.options:
                                        for option in item.options:
                                            if clicked_circle == option.pos:
                                                # Mouse mode
                                                if option.modable:
                                                    grid.set_mouse_mode(option)
                                                # --------------------------------------------------------------- #
                                                #                       CLICK DEFAULT OPTIONS                     #
                                                # --------------------------------------------------------------- #
                                                if option in item.default_options:
                                                    if option.name == "bag":
                                                        print "Gimme the loot!"
                                                    elif option.name == "mitosis":
                                                        item.mitosis(grid)
                                                    # Setting the mode
                                                    item.set_mode(grid, option)
                                                # --------------------------------------------------------------- #
                                                #                        CLICK SUB-OPTIONS                        #
                                                # --------------------------------------------------------------- #
                                                elif option in grid.mode_vs_options[item.mode]:
                                                    if item.mode == "move":
                                                        item.gen_move_track(grid, grid.mode_vs_options[item.mode].index(option))
                                                    elif option.name == "see":
                                                        item.range += 3
                                                        print "seen"
                                                    elif option.name == "smel":
                                                        print "sniff hair"
                                                    elif option.name == "medi":
                                                        item.range += 3
                                                        item.change_speed(10)
                                                    elif option.name == "audio":
                                                        item.range += 1
                                                    elif option.name == "eat":
                                                        item.change_speed(-1)
                                                    # Close menu when sub-option selected
                                                    item.set_in_menu(grid, False)
                                                # Close menu if option has no sub-options
                                                if option.name not in grid.mode_vs_options.keys():
                                                    item.set_in_menu(grid, False)
                                # Clicked outside
                                elif (clicked_circle != item.pos) and (clicked_circle not in grid.adj_tiles(item.pos)):
                                    item.set_in_menu(grid, False)
                # Debug print
                cir_utils.debug_print_click(grid, MOUSE_POS, clicked_circle, my_body)

        # --------------------------------------------------------------- #
        #                                                                 #
        #                             DRAWING                             #
        #                                                                 #
        # --------------------------------------------------------------- #
        cir_draw.draw_background(grid)
        # --------------------------------------------------------------- #
        #                           GAME MENU                             #
        # --------------------------------------------------------------- #
        if grid.game_menu:
            if grid.buttons:
                cir_draw.draw_menu_buttons(pygame, grid, MOUSE_POS)
        else:
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
            # Items
            for item in grid.items:
                if item.available:

                    # Radar
                    if item.radar_track:
                        cir_draw.draw_radar(pygame, grid, item)
                    # Items
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
                    if item.timer:
                        cir_draw.draw_timers(pygame, grid, my_body)

            # Mouse
            if grid.mouse_mode:
                cir_draw.draw_mouse_image(pygame, grid, MOUSE_POS)

        # End drawing
        pygame.display.update()

        # --------------------------------------------------------------- #
        #                                                                 #
        #                           CHANGE VARS                           #
        #                                                                 #
        # --------------------------------------------------------------- #

        # Rooms
        grid.load_room(my_body)

        # Check bag
        if "bag" in grid.everything.keys():
            cir_item_effects.empty_bag(grid)
        # Lifespan timer
        if grid.everything['lifespan'].is_over:
            # TODO: Avoid rerunning the script
            grid.game_over = True
            sys.argv.append('Game Over')
            os.execv(sys.executable, [sys.executable] + sys.argv)

        # Items
        for item in grid.items:
            if item.available:
                # Overlap
                item.overlapping(grid)
                # Movement
                if item.move_track:
                    item.move()
                if item.timer:
                    item.timer.tick()

                # Clean placeholders
                grid.clean_placeholders(item)

        # FPS
        pygame.time.Clock().tick(grid.fps)
    # END
    pygame.quit()
    quit()

# --------------------------------------------------------------- #
#                                                                 #
#                              MAIN                               #
#                                                                 #
# --------------------------------------------------------------- #
if __name__ == '__main__':
    # Loading
    scenario = cir_utils.set_scenario(sys.argv)
    grid = cir_grid.Grid(pygame)
    images = cir_cosmetic.Images(grid, pygame)
    fonts = cir_cosmetic.Fonts(grid, pygame)
    my_body = cir_loader.load_items(grid, images, fonts, scenario)
    # Settings
    cir_utils.set_argv(grid, sys.argv)
    # Start
    game_loop()
