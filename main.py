#######################################################################################################################
#################                                                                                     #################
#################                                 Main file                                           #################
#################                                                                                     #################
#######################################################################################################################
import os
import sys
import time
import pygame

from cir import cir_utils
from cir import cir_item_body
from cir import cir_grid
from cir import cir_draw
from cir import cir_cosmetic
from cir.cir_loader import load_all_items

pygame.init()

# LOADING GRID
grid = cir_grid.Grid()
grid.game_display = pygame.display.set_mode((grid.display_width, grid.display_height))

# LOADING IMAGES AND FONTS
images = cir_cosmetic.Images(grid, pygame)
fonts = cir_cosmetic.Fonts(grid, pygame)

# LOADING MY BODYeeeee
my_body = cir_item_body.BodyItem(grid=grid, name="my body", image=images.galab, pos=grid.center_tile, color=grid.dark_grey, speed=2)
grid.items.append(my_body)
grid.bodies.append(my_body)

# LOADING ALL ITEMS
ALL_ITEMS, MODE_VS_OPTIONS = load_all_items(grid, images, fonts, my_body)

# GAME SETTINGS
pygame.display.set_caption(grid.caption)
clock = pygame.time.Clock()
pygame.mouse.set_visible(True)


def gen_movement_arrows(event):
    """ Generates steps to move my body - gen_move_track() """
    move_options = MODE_VS_OPTIONS["move"]
    arrows = [pygame.K_w, pygame.K_e, pygame.K_d, pygame.K_s, pygame.K_a, pygame.K_q]
    for idx, arrow in enumerate(arrows):
        if event.key == arrow:
            if not my_body.move_track and not my_body.radar_track:
                my_body.gen_move_track(idx)
                if my_body.move_track:
                    my_body.img = eval("images.galab"+str(idx+1))



# TODO: Item generation algorithm on radar vs metrics
# TODO: Make a mouse class
# TODO: Make a mini map
# TODO: Make a signal method
# TODO: Log all statistics during a lifespan
# TODO: Create spirit mode, where karma is calculated
# TODO: Create pause menu before and while playing
# TODO: Log all events and show the last 3 on screen
# TODO: Fix track
# TODO: Create save button
# TODO: Show animated instructions
# TODO: Animate item generation
# TODO: Make installable exe file for the game



def game_loop():
    """ Main game loop. """

    GAME_EXIT = False
    START_TIME = time.time()
    grid.game_menu = True


    # Start
    while not GAME_EXIT:
        MOUSE_POS = pygame.mouse.get_pos()

        # Seconds in game
        cir_utils.seconds_in_game(grid, START_TIME)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GAME_EXIT = True

            if event.type == pygame.KEYDOWN:
                # =============================================================== #
                #                        ESCAPE LOOP                              #
                # =============================================================== #
                if event.key == pygame.K_ESCAPE:
                    if not grid.game_menu:
                        grid.game_menu = True

                    elif grid.game_menu and grid.seconds_in_game > 0:
                        grid.game_menu = False
                # =============================================================== #
                #                        SPACEBAR EVENTS                          #
                # =============================================================== #
                if event.key == pygame.K_SPACE:
                    if not grid.game_menu:

                        # Radar track populating
                        if not my_body.move_track and not my_body.in_menu and not my_body.radar_track:
                            my_body.gen_radar_track()

                        # TODO: time modifier
                        # lifespan.len_step += (lifespan.len_step / 100) * 10
                        # lifespan.step += 15
                        # print "steps:", lifespan.number_of_steps

                    # Debug
                    cir_utils.debug_print_space(grid)

                # =============================================================== #
                #                      Generate Movement                          #
                # =============================================================== #
                if not grid.game_menu and not my_body.in_menu:
                    gen_movement_arrows(event)

            # =============================================================== #
            #                           CLICK EVENTS                          #
            # =============================================================== #
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_circle = grid.mouse_in_tile(MOUSE_POS)
                if clicked_circle:

                    # ========== MENU BUTTONS ========== #
                    if grid.game_menu:
                        for button in grid.buttons:
                            if clicked_circle == button.pos:

                                if button.name == "play":
                                    grid.game_menu = False
                                    if grid.game_over:
                                        grid.game_over = False

                                elif button.name == "quit":
                                    pygame.quit()
                                    quit()

                    # =========== GRID ITEMS =========== #
                    elif not grid.game_menu:
                        for item in grid.items:
                            # Set in_menu for the items with menu (my_body)
                            item.check_in_menu(clicked_circle, MODE_VS_OPTIONS)
                            # Setting option positions
                            item.set_option_pos()
                            # Option clicked
                            if item.in_menu:

                                # Mouse mode image
                                grid.mouse_mode = None
                                grid.mouse_img = None

                                if item.options:
                                    for option in item.options:
                                        if clicked_circle == option.pos:

                                            # DEFAULT OPTIONS
                                            if option in item.default_options:

                                                if option.name == "bag":
                                                    print "Gimme the loot!"

                                                if option.name == "mitosis":
                                                    item.mitosis()

                                                item.set_mode(option, MODE_VS_OPTIONS)

                                            # SUBOPTIONS
                                            elif option in MODE_VS_OPTIONS[item.mode]:

                                                if item.mode == "move":
                                                    # TODO: fix below movement on arrows click
                                                    # item.gen_move_track(option.name, MODE_VS_OPTIONS[item.mode])
                                                    pass

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
                                                    # grid.tile_radius = 10

                                                # Close menu if option selected
                                                item.set_in_menu(False)
                                            # Close menu if option has no suboptions
                                            if option.name not in MODE_VS_OPTIONS.keys():
                                                item.set_in_menu(False)

                                            # Mouse mode image
                                            if option.modable:
                                                grid.mouse_mode = option.name
                                                if option.img and option.modable:
                                                    grid.mouse_img = option.img
                # Debug
                cir_utils.debug_print_click(grid, MOUSE_POS, clicked_circle, my_body)

        # =============================================================== #
        #                        DRAWING BACKGROUND                       #
        # =============================================================== #

        grid.game_display.fill(grid.dark_grey)

        if not grid.game_menu:
            # Revealed radius
            if grid.revealed_radius:
                cir_draw.draw_revealed_radius(pygame, grid)

            cir_draw.draw_mask(pygame, grid)

            # Grid
            if grid.show_grid:
                cir_draw.draw_grid(pygame, grid)

            # Playing board:
            if grid.show_playing_tiles:
                cir_draw.draw_playing_tiles(pygame, grid)

            # =============================================================== #
            #                        DRAWING ANIMATIONS                       #
            # =============================================================== #
            for item in grid.items:

                # Radar
                if item.radar_track:
                    cir_draw.draw_radar(pygame, grid, item)

                # Bodies
                # if (item.pos in grid.revealed_tiles) or (item == my_body):
                # TODO: fix drawing above items (overlap?)
                if (item.pos in grid.revealed_tiles) or (item in grid.bodies):
                    cir_draw.draw_body(pygame, grid, MOUSE_POS, item)

                # Item options
                if item.in_menu:
                    cir_draw.draw_item_options(pygame, grid, MOUSE_POS, item)



                # Show movement track in color
                if grid.show_movement and len(item.move_track) > 1:
                    cir_draw.draw_movement(pygame, grid, item)

            # Timers
            if grid.timers:
                cir_draw.draw_timers(pygame, grid, my_body)

        elif grid.game_menu:
            # Menu Buttons
            if grid.buttons:
                cir_draw.draw_menu_buttons(pygame, grid, MOUSE_POS)

        # Mouse Item
        # TODO: Create MouseItem
        # pygame.draw.circle(grid.game_display, grid.white, MOUSE_POS, 2, 0)
        if grid.mouse_mode:
            cir_draw.draw_mouse_image(pygame, grid, MOUSE_POS)


        # === END DRAWING === #
        pygame.display.update()

        # =============================================================== #
        #                           CHANGE VARS                           #
        # =============================================================== #
        if not grid.game_menu:

            # Lifespan timer
            if grid.timers:
                for timer in grid.timers:
                    timer.tick()

            for item in grid.items:

                # Movement
                if item.move_track:
                    item.move()
                else:
                    if item == my_body:
                        my_body.img = images.galab

            # Timers
            if grid.timers:
                for timer in grid.timers:
                    if timer.is_over:
                        # Lifespan
                        if timer.name == "lifespan":
                            grid.game_over = True
                            # TODO: add sys argv for gameover and loading a game
                            os.execv(sys.executable, [sys.executable] + sys.argv)

        # FPS
        clock.tick(grid.fps)

    # == END == #
    pygame.quit()
    quit()

if __name__ == '__main__':
    game_loop()
