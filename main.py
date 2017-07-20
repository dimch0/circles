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
# TODO: Create a reversed timer
# TODO: Create timer for seconds in game
# TODO: Improve movement by checking each next tile while direction
# TODO: Check if two circles are crossing
# TODO: Indicate uses
# TODO: Item generation
# TODO: Create mini map
# TODO: Create signal function
# TODO: Log statistics during a lifespan
# TODO: Create spirit mode, calculate karma
# TODO: Log messages on screen
# TODO: Create save button
# TODO: Create load button
# TODO: Create resume button
# TODO: Create installation .exe file
# --------------------------------------------------------------- #
#                            Animation                            #
# --------------------------------------------------------------- #
# TODO: Add moving image
# TODO: Animate item generation
# TODO: Animate item activation
# TODO: Animate menu opening
# TODO: Animate room transition
# TODO: Animate circle kiss
# TODO: Animate instructions
# TODO: Animate moving circle
# --------------------------------------------------------------- #
#                            Bug fixes                            #
# --------------------------------------------------------------- #
# TODO: Fix closing menu on eye radar / Proposa: add clickable


# --------------------------------------------------------------- #
#                            Imports                              #
# --------------------------------------------------------------- #
import os
import sys
import time
# --------------------------------------------------------------- #
#                             Pygame                              #
# --------------------------------------------------------------- #
import pygame
pygame.init()
# --------------------------------------------------------------- #
#                           CIR modules                           #
# --------------------------------------------------------------- #
from cir import cir_grid
from cir import cir_draw
from cir import cir_utils
from cir import cir_loader
from cir import cir_cosmetic
from cir import cir_item_effects


def game_loop():
    """ Main game loop """

    print "Game started"
    GAME_EXIT = False
    START_TIME = time.time()

    while not GAME_EXIT:

        MOUSE_POS = pygame.mouse.get_pos()
        current_tile = grid.mouse_in_tile(MOUSE_POS) if grid.mouse_in_tile(MOUSE_POS) else None
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
                        my_body.gen_radar_track(grid)
                        # Debug
                        cir_utils.debug_print_space(grid)

                    elif event.key == pygame.K_t:
                        print ">>>> key t"
                        # Lifespan timer
                        lst.update(-1)
                        print "duration        :", lst.duration
                        print "current    step :", lst.step
                        print "number of steps :", lst.number_of_steps
                        print "start   degrees :", lst.start_degrees
                        print "filled  degrees :", lst.filled_degrees
                        print "step    degrees :", lst.step_degrees
                        print "-" * 35

                    elif event.key == pygame.K_l:
                        print ">>>> key l"
                        grid.game_over = True
                        sys.argv.append('Scenario_2')
                        os.execv(sys.executable, [sys.executable] + sys.argv)

                    elif event.key == pygame.K_1:
                        print ">>>> key 1"
                        grid.change_room(1)

                    elif event.key == pygame.K_2:
                        print ">>>> key 2"
                        grid.change_room(2)

                    elif event.key == pygame.K_3:
                        print ">>>> key 3"
                        grid.change_room(3)

                    elif event.key == pygame.K_k:
                        print ">>>> key k"
                        my_body.img = images.alien1
                        my_body.default_img = my_body.img
                        my_body.speed = 10

                    # Movement Population
                    elif not my_body.in_menu:
                        my_body.gen_movement_arrows(pygame, grid, event)

            # --------------------------------------------------------------- #
            #                                                                 #
            #                          CLICK EVENTS                           #
            #                                                                 #
            # --------------------------------------------------------------- #

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_tile:
                    # --------------------------------------------------------------- #
                    #                            GAME MENU                            #
                    # --------------------------------------------------------------- #
                    if grid.game_menu:
                        for button in grid.buttons:
                            if current_tile == button.pos and button.available:
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
                            cir_item_effects.laino_mode_click(grid, current_tile)
                        elif grid.mouse_mode == "shit":
                            cir_item_effects.shit_mode_click(grid, current_tile)
                        elif grid.mouse_mode == "see":
                            cir_item_effects.produce(grid, "observer", current_tile)
                            grid.everything["observer"].timer.restart()

                        # --------------------------------------------------------------- #
                        #                          CLICK ON ITEMS                         #
                        # --------------------------------------------------------------- #
                        for item in grid.items:
                            if item.available:
                                if current_tile == item.pos:
                                    # --------------------------------------------------------------- #
                                    #                            BAG MODE                             #
                                    # --------------------------------------------------------------- #
                                    if grid.mouse_mode == "bag":
                                        print "HERE", grid.mouse_mode, item.name, item.collectable
                                        cir_item_effects.collect(grid, item)

                                    # Set in_menu for the items with menu (my_body)
                                    item.check_in_menu(grid, current_tile)
                                    # Setting option positions
                                    item.set_option_pos(grid)
                                    # Option clicked
                                    if item.in_menu:
                                        grid.clean_mouse()

                                # --------------------------------------------------------------- #
                                #                       CLICK ITEM OPTIONS                        #
                                # --------------------------------------------------------------- #
                                elif current_tile in grid.adj_tiles(item.pos) and item.in_menu:
                                    if item.options:
                                        for option in item.options:
                                            if current_tile == option.pos:

                                                # --------------------------------------------------------------- #
                                                #                           Mouse mode                            #
                                                # --------------------------------------------------------------- #
                                                if option.modable:
                                                    grid.set_mouse_mode(option)

                                                # --------------------------------------------------------------- #
                                                #                       CLICK DEFAULT OPTIONS                     #
                                                # --------------------------------------------------------------- #
                                                if option in item.default_options:
                                                    # bag
                                                    if option.name == "bag":
                                                        print "Gimme the loot!"
                                                    # mitosis
                                                    elif option.name == "mitosis":
                                                        item.mitosis(grid)
                                                    # enter / exit
                                                    elif any(a for a in ["enter_", "exit_"] if a in option.name):
                                                        cir_item_effects.enter_exit(grid, my_body, item, option)

                                                    # Setting the mode
                                                    item.set_mode(grid, option)


                                                # --------------------------------------------------------------- #
                                                #                        CLICK SUB-OPTIONS                        #
                                                # --------------------------------------------------------------- #
                                                elif option in grid.mode_vs_options[item.mode]:
                                                    # move
                                                    if item.mode == "move":
                                                        item.gen_move_track(grid, grid.mode_vs_options[item.mode].index(option))
                                                    # see
                                                    elif option.name == "see":
                                                        # item.range += 3
                                                        print "seen"
                                                    # smel
                                                    elif option.name == "smel":
                                                        print "sniff hair"
                                                    # medi
                                                    elif option.name == "medi":
                                                        item.range += 3
                                                        my_body.gen_radar_track(grid)
                                                        item.range -= 3
                                                    # audio
                                                    elif option.name == "audio":
                                                        item.range += 1
                                                    # eat
                                                    elif option.name == "eat":
                                                        item.change_speed(-1)
                                                    # touch
                                                    elif option.name == "touch":
                                                        item.change_speed(1)
                                                    # Close menu when sub-option selected
                                                    item.set_in_menu(grid, False)
                                                # Close menu if option has no sub-options
                                                if option.name not in grid.mode_vs_options.keys():
                                                    item.set_in_menu(grid, False)
                                # Clicked outside
                                elif (current_tile != item.pos) and (current_tile not in grid.adj_tiles(item.pos)):
                                    item.set_in_menu(grid, False)
                # Debug print
                cir_utils.debug_print_click(grid, MOUSE_POS, current_tile, my_body)

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
                        cir_draw.draw_timers(pygame, grid, item)

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
        if not grid.game_menu:

            # My_body to room
            if not my_body in grid.items:
               grid.items.append(my_body)

            # Check bag
            if "bag" in grid.everything.keys():
                cir_item_effects.empty_bag(grid)

            # Lifespan timer
            if grid.everything['lifespan'].is_over:
                cir_item_effects.lifespan_over_effect(grid, sys, os)

            # Items
            for item in grid.items:
                # Timers
                if item.timer and item.available:
                    item.timer.tick()

                # Eyespan timer
                if item.name == "observer":
                    if item.timer.is_over:
                        cir_item_effects.observer_effect(grid,item)

                if item.available:
                    # Movement
                    if item.move_track:
                        item.move()

                    # Clean placeholders
                    grid.clean_placeholders(item)
                    # Overlap
                    item.overlapping(grid)


    # --------------------------------------------------------------- #
    #                          FINISH LOOP                            #
    # --------------------------------------------------------------- #
        grid.clock.tick(grid.fps)

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
    grid.game_menu = False
    images = cir_cosmetic.Images(grid, pygame)
    fonts = cir_cosmetic.Fonts(grid, pygame)
    my_body = cir_loader.load_items(grid, images, fonts, scenario)
    grid.load_current_room()
    # Settings
    cir_utils.set_argv(grid, sys.argv)

    # TESTING
    lst = grid.everything["lifespan"]
    lst.duration = 60

    # Start
    game_loop()
