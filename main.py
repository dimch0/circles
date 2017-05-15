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
from cir import cir_body
from cir import cir_grid
from cir import cir_draw
from cir import cir_cosmetic
from cir.cir_loader import load_all_items

pygame.init()

# LOADING GRID
grid = cir_grid.Grid()

# LOADING IMAGES AND FONTS
images = cir_cosmetic.Images(grid)
fonts = cir_cosmetic.Fonts(grid)

# LOADING MY BODY
my_body = cir_body.BodyItem(grid=grid, name="my body", pos=grid.center_tile, color=grid.pink, speed=2)
grid.items.append(my_body)

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
            my_body.direction = move_options[idx].name

    if my_body.direction and not my_body.move_track and not my_body.radar_track:
        my_body.gen_move_track(my_body.direction, move_options)



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
                # ========================================= ESCAPE LOOP ============================================= #
                if event.key == pygame.K_ESCAPE:
                    if not grid.game_menu:
                        grid.game_menu = True

                    elif grid.game_menu and grid.seconds_in_game > 0:
                        grid.game_menu = False
                # ========================================= SPACE BAR EVENTS ======================================== #
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

                # ========================================= GENERATE MOVEMENT ======================================= #
                if not grid.game_menu and not my_body.in_menu:
                    gen_movement_arrows(event)


            # ============================================= CLICK EVENTS ============================================ #
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

                                elif button.name == "replay":
                                    os.execv(sys.executable, [sys.executable] + sys.argv)

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
                                if item.options:
                                    for option in item.options:
                                        if clicked_circle == option.pos:

                                            # If default option -> set mode
                                            if option in item.default_options:
                                                item.set_mode(option, MODE_VS_OPTIONS)

                                            # Check option specifics
                                            elif option in MODE_VS_OPTIONS[item.mode]:

                                                if item.mode == "move":
                                                    item.gen_move_track(option.name, MODE_VS_OPTIONS[item.mode])

                                                elif option.name == "see":
                                                    item.range += 1
                                                    # item.mode = "seen"

                                                elif option.name == "smel":
                                                    item.change_speed(1)

                                                elif option.name == "medi":
                                                    item.range += 3

                                                elif option.name == "audio":
                                                    item.change_speed(10)

                                                elif option.name == "eat":
                                                    item.change_speed(-1)
                                                # Close menu if option selected
                                                item.set_in_menu(False)
                # Debug
                cir_utils.debug_print_click(grid, MOUSE_POS, clicked_circle, my_body)

        # ======================== DRAWING BACKGROUND ======================= #
        # Background
        grid.game_display.fill(grid.grey)

        if not grid.game_menu:
            # Revealed radius
            if grid.revealed_radius:
                cir_draw.draw_revealed_radius(grid)

            cir_draw.draw_mask(grid)

            # Grid
            if grid.show_grid:
                cir_draw.draw_grid(grid)

            # Playing board:
            if grid.show_playing_tiles:
                cir_draw.draw_playing_tiles(grid)

        # ======================== DRAWING ANIMATIONS ======================= #
        if not grid.game_menu:
            for item in grid.items:

                # Radar
                if item.radar_track:
                    cir_draw.draw_radar(item, grid)

                # Item options
                if item.in_menu:
                    cir_draw.draw_item_options(item, grid, MOUSE_POS)

                # Bodies
                if (item.pos in grid.revealed_tiles) or (item == my_body):
                    if item.color:
                        cir_draw.draw_body(item, MOUSE_POS, grid)

                # Show movement track in color
                if grid.show_movement and len(item.move_track) > 1:
                    cir_draw.draw_movement(item, grid)

            # Timers
            if grid.timers:
                cir_draw.draw_timers(grid, my_body)

        elif grid.game_menu:
            # Menu Buttons
            if grid.buttons:
                cir_draw.draw_menu_buttons(MOUSE_POS, grid)

        # Mouse Item
        # TODO: Create MouseItem
        # pygame.draw.circle(grid.game_display, grid.white, MOUSE_POS, 2, 0)
        # for tile in grid.tiles:
        #     cir_draw.draw_hover(tile, MOUSE_POS, grid, grid.game_display)

        # === END DRAWING === #
        pygame.display.update()

        # ================================================ CHANGE VARS ============================================== #
        if not grid.game_menu:

            # Lifespan timer
            if grid.timers:
                for timer in grid.timers:
                    timer.tick()

            for item in grid.items:

                # Movement
                if item.move_track:
                    item.move()

            # Timers
            if grid.timers:
                for timer in grid.timers:
                    if timer.is_over:
                        # Lifespan
                        if timer.name == "lifespan":
                            grid.game_over = True
                            grid.game_menu = True
                            os.execv(sys.executable, [sys.executable] + sys.argv)

        # FPS
        clock.tick(grid.fps)

    # == END == #
    pygame.quit()
    quit()

if __name__ == '__main__':
    game_loop()
