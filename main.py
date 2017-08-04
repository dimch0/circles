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
# TODO: Item generation
# TODO: Level Editor
# TODO: Log messages on screen
# TODO: Create map (screenshot all rooms) room 401
# TODO: Create inside body view room 400
# TODO: Create spirit mode NEW SCENARIO
# TODO: Log statistics during a lifespan, calculate karma
# TODO: Create save button
# TODO: Create load button
# TODO: Create installation .exe file
# TODO: Create reverse get position
# --------------------------------------------------------------- #
#                            Animation                            #
# --------------------------------------------------------------- #
# TODO: Indicate uses / meters
# TODO: Animate item activation
# TODO: Animate demo
# TODO: Add sounds
# --------------------------------------------------------------- #
#                            Bug fixes                            #
# --------------------------------------------------------------- #
# TODO: Fix mitosis (occ prop lag, overlap, birth fat) Move to effects
# TODO: Fix item collection
# --------------------------------------------------------------- #
#                            Imports                              #
# --------------------------------------------------------------- #
import time
import pygame
pygame.init()
from cir import cir_utils
from cir import cir_grid
from cir import cir_cosmetic
from cir.cir_draw import GameDrawer
from cir.cir_loader import DataLoader
from cir.cir_effects import GameEffects


def game_loop(game_over, scenario="Scenario_1"):
    # --------------------------------------------------------------- #
    #                                                                 #
    #                            LOADING                              #
    #                                                                 #
    # --------------------------------------------------------------- #
    grid            = cir_grid.Grid(pygame, scenario)
    grid.images     = cir_cosmetic.Images(grid, pygame)
    grid.fonts      = cir_cosmetic.Fonts(grid, pygame)
    loader          = DataLoader(grid)
    drawer          = GameDrawer(grid, pygame)
    effects         = GameEffects(grid, loader)
    my_body         = loader.load_items()
    grid.start_time = time.time()

    if game_over:
        grid.rename_button("play", "replay")
    if scenario == "Scenario_2":
        grid.game_menu = False

    # --------------------------------------------------------------- #
    #                         TEST TESTING PLACE                      #
    # --------------------------------------------------------------- #
    my_body.lifespan.duration = 60


    print "Game started"
    while not grid.game_over:

        current_tile = grid.mouse_in_tile(pygame.mouse.get_pos())

        grid.seconds_in_game_tick()

        # --------------------------------------------------------------- #
        #                                                                 #
        #                            EVENTS                               #
        #                                                                 #
        # --------------------------------------------------------------- #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # --------------------------------------------------------------- #
            #                            KEY EVENTS                           #
            # --------------------------------------------------------------- #
            elif event.type == pygame.KEYDOWN:
                # --------------------------------------------------------------- #
                #                             'Esc'                               #
                # --------------------------------------------------------------- #
                if event.key == pygame.K_ESCAPE:
                    if not grid.game_menu:
                        grid.game_menu = True
                        grid.rename_button("replay", "play")
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
                        cir_utils.debug_print_space(grid, my_body)

                    elif event.key == pygame.K_t:
                        print ">>>> key t"
                        my_body.vibe_speed += 0.1
                        my_body.lifespan.update(5)
                        print my_body.lifespan.duration

                    elif event.key == pygame.K_KP_ENTER:
                        print "EDITOR MODE"
                        my_body.lifespan = None
                        for editor in grid.everything.values():
                            if "EDITOR" in editor.name:
                                if not editor in grid.items:
                                    grid.items.append(editor)

                    elif event.key == pygame.K_f:
                        print ">>>> key f"
                        my_body.gen_fat()

                    elif event.key == pygame.K_p:
                        print ">>>> key p"
                        my_body.lifespan.update(-1)
                        print my_body.lifespan.duration

                    elif event.key == pygame.K_l:
                        print ">>>> key l"
                        scenario = 'Scenario_2'
                        grid.game_over = True

                    elif event.key == pygame.K_k:
                        print ">>>> key k"
                        my_body.img = grid.images.alien1
                        my_body.default_img = my_body.img
                        my_body.speed = 10


                    elif event.key == pygame.K_1:
                        print ">>>> key 1"
                        grid.change_room(1)

                    elif event.key == pygame.K_2:
                        print ">>>> key 2"
                        grid.change_room(2)

                    elif event.key == pygame.K_3:
                        print ">>>> key 3"
                        grid.change_room(3)


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
                            if current_tile == button.pos and button.clickable:
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
                        effects.mouse_mode_click(current_tile, my_body)

                        # --------------------------------------------------------------- #
                        #                          CLICK ON ITEMS                         #
                        # --------------------------------------------------------------- #
                        for item in grid.items:
                            if item.clickable:
                                if current_tile == item.pos:
                                    # Setting the mouse mode
                                    if item.modable:
                                        grid.set_mouse_mode(item)
                                    # --------------------------------------------------------------- #
                                    #                    MOUSE MODE CLICK ON ITEM                     #
                                    # --------------------------------------------------------------- #
                                    effects.mouse_mode_click_item(item)

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
                                                effects.click_options(item, option, my_body)

                                # Clicked outside
                                elif (current_tile != item.pos) and (current_tile not in grid.adj_tiles(item.pos)):
                                    item.set_in_menu(grid, False)

                # Debug print
                cir_utils.debug_print_click(grid, current_tile, my_body)

        # --------------------------------------------------------------- #
        #                                                                 #
        #                             DRAWING                             #
        #                                                                 #
        # --------------------------------------------------------------- #
        # Game Menu
        if grid.game_menu:
            if grid.buttons:
                drawer.draw_menu_buttons(current_tile)
        else:
            # BACKGROUND
            drawer.draw_background_stuff()
            # ANIMATIONS
            drawer.draw_animations(my_body, current_tile)

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
                effects.empty_bag()

            # Items
            for item in grid.items:

                # Timers
                effects.timer_effect(item)

                # Enter
                effects.enter_room(my_body, item)

                # Destruction
                effects.destruction(item)

                if item.available:

                    # Kissing circles
                    if item.type == 'body':
                        for adj_item in grid.items:
                            if adj_item.type == 'body' and adj_item.pos in grid.adj_tiles(item.pos):
                                item.gen_fat()

                    # Movement
                    if item.direction != None:
                        item.gen_move_track(grid)
                    if item.move_track:
                        item.move()

                    # Signal hit
                    if effects.signal_hit(item, my_body):
                        effects.signal_hit_effect(item)

                    # Clean placeholders
                    grid.clean_placeholders(item)
                    # Overlap
                    item.overlapping(grid)

        # Finish Loop
        grid.clock.tick(grid.fps)

    if grid.game_over:
        game_loop(grid.game_over, scenario)

    pygame.quit()
    quit()

# --------------------------------------------------------------- #
#                                                                 #
#                              MAIN                               #
#                                                                 #
# --------------------------------------------------------------- #
if __name__ == '__main__':
    game_loop(game_over=False)
