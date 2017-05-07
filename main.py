#######################################################################################################################
#################                                                                                     #################
#################                                 Main file                                           #################
#################                                                                                     #################
#######################################################################################################################
import os
import sys
import time
import pygame

from cir import cir_body
from cir import cir_grid
from cir import cir_utils
from cir import cir_cosmetic
from cir import cir_item
from cir import cir_timer
from cir import cir_mobile
from cir import cir_button
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
gameDisplay = pygame.display.set_mode((grid.display_width, grid.display_height))
pygame.display.set_caption(grid.caption)
clock = pygame.time.Clock()
pygame.mouse.set_visible(True)


def seconds_in_game(START_TIME):
    """ Counts the seconds in the game """
    # TODO: FIX START TIME AND PAUSE SECONDS
    if not grid.game_menu:
        if time.time() + grid.seconds_in_pause > (START_TIME + grid.seconds_in_game) - grid.seconds_in_pause:
            print "second: {0}".format(grid.seconds_in_game)
            grid.seconds_in_game += 1


def draw_radar(item):
    """ Radar animation """
    radar_radius, thick = item.radar()
    if radar_radius and thick:
        pygame.draw.circle(gameDisplay, item.grid.green, item.pos, radar_radius, thick)


def draw_revealed_radius():
    """ Drawing the revealed areas """
    for revealed in grid.revealed_radius:
        pygame.draw.circle(gameDisplay, grid.ungrey, revealed[0], revealed[1], 0)
        printed = revealed
        if printed:
            for to_be_printed in grid.revealed_radius:
                if printed[0] == to_be_printed[0]:
                    if printed[1] < to_be_printed[1]:
                        grid.revealed_radius.remove(printed)


def draw_item_options(item, MOUSE_POS):
    """ Draws the item menu options """

    for option in item.options:
        if option.color:
            pygame.draw.circle(gameDisplay, option.color, option.pos, grid.tile_radius, option.border)
        if option.img:
            gameDisplay.blit(option.img, option.set_img_pos())
        draw_hover(option.pos, MOUSE_POS)

def draw_menu_buttons(MOUSE_POS):
    """ Drawing the buttons in the game menu """

    for button in grid.buttons:
        if button.color:
            pygame.draw.circle(gameDisplay, button.color, button.pos, grid.tile_radius, button.border)
        if button.img:
            gameDisplay.blit(button.img, button.set_img_pos())
        if button.text:
            gameDisplay.blit(button.text, button.text_rect)
        draw_hover(button.pos, MOUSE_POS)


def draw_body(item, MOUSE_POS):
    """ Draws each body and it's image if available """
    pygame.draw.circle(gameDisplay, item.color, item.pos, grid.tile_radius, item.border)
    if item.img:
        gameDisplay.blit(item.img, item.set_img_pos())
    draw_hover(item.pos, MOUSE_POS)

def draw_timers():
    """ Draws current state of a timer """
    # pygame.draw.circle(gameDisplay, timer.color, timer.pos, grid.tile_radius, 0)
    for timer in grid.timers:
        if timer.name == "lifespan":
            timer.pos = my_body.pos
        pygame.draw.arc(gameDisplay, timer.time_color, timer.rect, timer.filled_angle, timer.start_point, 2)


def draw_grid():
    """ Shows the grid tiles in white """
    for tile in grid.tiles:
        pygame.draw.circle(gameDisplay, grid.ungrey, tile, grid.tile_radius, 1)

    draw_playing_tiles()



def draw_mask():
    rect1 = [
        (0,0),
        (grid.center_tile[0] - ((4 * grid.cathetus) + (grid.cathetus / 2) + 5), (grid.display_height))
            ]
    rect2 = [
        (grid.center_tile[0] + ((4 * grid.cathetus) + (grid.cathetus / 2) + 5), 0),
        (grid.center_tile[0], grid.display_height)
            ]
    tri1 = [
        (grid.center_tile[0] - ((4 * grid.cathetus) + (grid.cathetus / 2) + 5), (grid.center_tile[0] - 14 * grid.tile_radius)),
        (grid.center_tile[0] - ((4 * grid.cathetus) + (grid.cathetus / 2) + 5), 0),
        (grid.center_tile[0] + ((2 * grid.cathetus) + (grid.cathetus / 2) + 5), 0)
    ]
    tri2 = [
        (grid.center_tile[0] + ((4 * grid.cathetus) + (grid.cathetus / 2) + 5), (grid.center_tile[0] - 14 * grid.tile_radius)),
        (grid.center_tile[0] + ((4 * grid.cathetus) + (grid.cathetus / 2) + 5), 0),
        (grid.center_tile[0] - ((2 * grid.cathetus) + (grid.cathetus / 2) + 5), 0)
    ]
    tri3 = [
        (grid.center_tile[0] - ((4 * grid.cathetus) + (grid.cathetus / 2) + 5), (grid.center_tile[0] - 5 * grid.tile_radius)),
        (grid.center_tile[0] - ((4 * grid.cathetus) + (grid.cathetus / 2) + 5), grid.display_height),
        (grid.center_tile[0] + ((2 * grid.cathetus) + (grid.cathetus / 2) + 5), grid.display_height)
    ]
    tri4 = [
        (grid.center_tile[0] + ((4 * grid.cathetus) + (grid.cathetus / 2) + 5), (grid.center_tile[0] - 5 * grid.tile_radius)),
        (grid.center_tile[0] + ((4 * grid.cathetus) + (grid.cathetus / 2) + 5), grid.display_height),
        (grid.center_tile[0] - ((2 * grid.cathetus) + (grid.cathetus / 2) + 5), grid.display_height)
    ]

    pygame.draw.rect(gameDisplay, grid.grey, rect1, 0)
    pygame.draw.rect(gameDisplay, grid.grey, rect2, 0)
    pygame.draw.polygon(gameDisplay, grid.grey, tri1, 0)
    pygame.draw.polygon(gameDisplay, grid.grey, tri2, 0)

    pygame.draw.polygon(gameDisplay, grid.grey, tri3, 0)
    pygame.draw.polygon(gameDisplay, grid.grey, tri4, 0)


def draw_hover(tile, MOUSE_POS):
    """ Highlights the hovered tile """
    if cir_utils.in_circle(tile, grid.tile_radius, MOUSE_POS):
        pygame.draw.circle(gameDisplay, grid.white, tile, grid.tile_radius + 1, 2)


def draw_movement(item):
    """ DEBUG: Shows the movement in cyan and the correct track in red """
    pygame.draw.line(gameDisplay, grid.azure, item.move_track[0], item.move_track[-1], 1)
    for o in item.move_track:
        pygame.draw.circle(gameDisplay, grid.white, o, 2, 1)


def draw_playing_tiles():
    """ Shows all tiles of the playing board in yellow """
    if grid.playing_tiles:
        for tile in grid.playing_tiles:
            pygame.draw.circle(gameDisplay, grid.gelb, tile, grid.tile_radius, 1)


def gen_movement_my_body(event):
    """ Generates steps to move my body - gen_move_track() """
    move_options = MODE_VS_OPTIONS["move"]
    arrows = [pygame.K_w, pygame.K_e, pygame.K_d, pygame.K_s, pygame.K_a, pygame.K_q]
    for idx, arrow in enumerate(arrows):
        if event.key == arrow:
            my_body.direction = move_options[idx].name

    if my_body.direction and not my_body.move_track and not my_body.radar_track:
        my_body.gen_move_track(my_body.direction, move_options)



def debug_print_click(MOUSE_POS, clicked_circle):
    """  Debug print on click event  """
    print(""">>>>>> click: {0}, tile: {1}
mode        : {2}
menu        : {3}
grid items  : {4}
occupado:   : {5}
playing     : {6}
move track  : {7}
all tiles   : {8}
speed       : {9}
""".format(MOUSE_POS,
           clicked_circle,
           my_body.mode,
           my_body.in_menu,
           [item.name for item in grid.items],
           grid.occupado_tiles,
           len(grid.playing_tiles),
           my_body.move_track,
           len(grid.tiles),
           my_body.speed
           )
          )


def debug_print_space():
    """  Debug print on space bar event  """
    print(""">>>> space
revealed tiles: {0}
revealed_radius: {0}
""".format(len(grid.revealed_tiles),
           len(grid.revealed_radius),
          )
         )


def game_loop():
    """ Main game loop. """

    GAME_EXIT = False
    START_TIME = time.time()
    grid.game_menu = True

    # Start
    while not GAME_EXIT:
        MOUSE_POS = pygame.mouse.get_pos()

        # Seconds in game
        seconds_in_game(START_TIME)

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
                    debug_print_space()

                # ========================================= GENERATE MOVEMENT ======================================= #
                if not grid.game_menu:
                    gen_movement_my_body(event)


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
                                                    item.range += 5

                                                elif option.name == "audio":
                                                    item.change_speed(10)

                                                elif option.name == "eat":
                                                    item.change_speed(-1)
                                                # Close menu if option selected
                                                item.set_in_menu(False)
                # Debug
                debug_print_click(MOUSE_POS, clicked_circle)

        # ======================== DRAWING BACKGROUND ======================= #
        # Background
        gameDisplay.fill(grid.grey)

        if not grid.game_menu:
            # Revealed radius
            if grid.revealed_radius:
                draw_revealed_radius()

            draw_mask()

            # Grid
            if grid.show_grid:
                draw_grid()

            # Playing board:
            # if grid.show_playing_tiles:
            #     draw_playing_tiles()

        # ======================== DRAWING ANIMATIONS ======================= #
        if not grid.game_menu:
            for item in grid.items:

                # Radar
                if item.radar_track:
                    draw_radar(item)

                # Item options
                if item.in_menu:
                    draw_item_options(item, MOUSE_POS)

                # Bodies
                if (item.pos in grid.revealed_tiles) or (item == my_body):
                    draw_body(item, MOUSE_POS)

                # Show movement track in color
                if grid.show_movement and len(item.move_track) > 1:
                    draw_movement(item)

            # Timers
            if grid.timers:
                draw_timers()

        elif grid.game_menu:
            # Menu Buttons
            if grid.buttons:
                draw_menu_buttons(MOUSE_POS)

        # Mouse Item
        # TODO: Create MouseItem
        # pygame.draw.circle(gameDisplay, grid.white, MOUSE_POS, 2, 0)
        # for tile in grid.tiles:
        #     draw_hover(tile, MOUSE_POS)

        # Update display ===== End drawing
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
