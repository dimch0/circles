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
# TODO: Indicate uses
# TODO: Item generation
# TODO: Create mini map
# TODO: Create signal function
# TODO: Log statistics during a lifespan
# TODO: Create spirit mode, calculate karma
# TODO: Log messages on screen
# TODO: Create save button
# TODO: Create load button
# TODO: Create installation .exe file
# --------------------------------------------------------------- #
#                            Animation                            #
# --------------------------------------------------------------- #
# TODO: Animate item activation
# TODO: Animate menu opening
# TODO: Animate room transition
# TODO: Animate circle kiss
# TODO: Animate instructions
# TODO: Animate moving circle
# --------------------------------------------------------------- #
#                            Bug fixes                            #
# --------------------------------------------------------------- #s
# TODO: Fix revert image rotation
# TODO: Fix occupado lag calculation propertyq
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


def game_loop(game_over):
    """ Main game loop """

    # TODO: If grid.game_over show replay buttons

    print "Game started"
    scenario = cir_utils.set_scenario(sys.argv)
    grid = cir_grid.Grid(pygame)

    images = cir_cosmetic.Images(grid, pygame)
    fonts = cir_cosmetic.Fonts(grid, pygame)
    my_body = cir_loader.load_items(grid, images, fonts, scenario)
    grid.start_time = time.time()
    my_body.gen_birth_track(grid)
    grid.rooms[grid.current_room]["revealed_radius"].append(((my_body.pos), grid.tile_radius))
    grid.load_current_room()
    if game_over:
        grid.everything["play"].available = False
        grid.everything["replay"].available = True

    my_body.timers["my_body_lifespan"].duration = 3

    while not grid.game_over:

        MOUSE_POS = pygame.mouse.get_pos()
        current_tile = grid.mouse_in_tile(MOUSE_POS) if grid.mouse_in_tile(MOUSE_POS) else None
        grid.seconds_in_game_tick()

        # --------------------------------------------------------------- #
        #                                                                 #
        #                            EVENTS                               #
        #                                                                 #
        # --------------------------------------------------------------- #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                grid.game_over = True
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
                        if grid.everything["replay"].available:
                            grid.everything["play"].available = True
                            grid.everything["replay"].available = False
                    elif grid.game_menu and grid.seconds_in_game > 0:
                        grid.game_menu = False

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
                        my_body.timers["my_body_lifespan"].update(5)
                        if scenario == "Scenario_2":
                            circle_1 = (my_body.pos, grid.tile_radius)
                            circle_2 = (grid.everything["bokluk"].pos, grid.tile_radius)
                            print cir_utils.intersecting(circle_1, circle_2)


                    elif event.key == pygame.K_l:
                        print ">>>> key l"

                        sys.argv.append('Scenario_2')
                        grid.game_over = True
                        grid.game_over = True
                        # os.execv(sys.executable, [sys.executable] + sys.argv)

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
                        if scenario == "Scenario_2":
                            grid.everything["bokluk"].pos = (
                                grid.everything["bokluk"].pos[0] - 1,
                                grid.everything["bokluk"].pos[1])
                            print grid.everything["bokluk"].pos

                    # Movement Population
                    elif not my_body.in_menu:
                        my_body.gen_direction(pygame, grid, event)

            # --------------------------------------------------------------- #
            #                                                                 #
            #                          CLICK EVENTS                           #
            #                                                                 #
            # --------------------------------------------------------------- #
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_tile:

                    # Game Menu
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
                        #                         MOUSE MODE CLICK                        #
                        # --------------------------------------------------------------- #
                        cir_item_effects.mouse_mode_click(grid, current_tile)

                        # --------------------------------------------------------------- #
                        #                          CLICK ON ITEMS                         #
                        # --------------------------------------------------------------- #
                        for item in grid.items:
                            if item.available:
                                if current_tile == item.pos:
                                    # --------------------------------------------------------------- #
                                    #                    MOUSE MODE CLICK ON ITEM                     #
                                    # --------------------------------------------------------------- #
                                    cir_item_effects.mouse_mode_click_item(grid, item)

                                    # --------------------------------------------------------------- #
                                    #                           MENU OPTIONS                          #
                                    # --------------------------------------------------------------- #
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

                                                # Setting the mouse mode
                                                if option.modable:
                                                    grid.set_mouse_mode(option)
                                                # --------------------------------------------------------------- #
                                                #                      OPTIONS / SUB-OPTIONS                      #
                                                # --------------------------------------------------------------- #
                                                cir_item_effects.click_options(grid, item, option, my_body)
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

        # Game Menu
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
            # TEST



            for item in grid.items:

                if item.available:
                    # Birth
                    cir_draw.draw_birth(grid, pygame, item)
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
                    if item.timers:
                        cir_draw.draw_timers(pygame, grid, item)

            # Item options
            for item in grid.items:
                if item.available:
                    if item.in_menu:
                        cir_draw.draw_item_options(pygame, grid, MOUSE_POS, item)

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
            # Items
            for item in grid.items:
                # Timers
                if item.timers:
                    for timer in item.timers.values():
                        timer.tick()
                        cir_item_effects.timer_effect(grid, item, timer)
                if item.available:
                    # Movement
                    if item.direction != None:
                        item.gen_move_track(grid)
                    if item.move_track:
                        item.move()
                    # Clean placeholders
                    grid.clean_placeholders(item)
                    # Overlap
                    item.overlapping(grid)

        # Finish Loop
        grid.clock.tick(grid.fps)

    if grid.game_over:
        game_loop(grid.game_over)

    pygame.quit()
    quit()

# --------------------------------------------------------------- #
#                                                                 #
#                              MAIN                               #
#                                                                 #
# --------------------------------------------------------------- #
if __name__ == '__main__':
    game_loop(game_over=False)
