#######################################################################################################################
#################                                                                                     #################
#################                                 Main file                                           #################
#################                                                                                     #################
#######################################################################################################################
import time
import pygame

from cir import cir_body, cir_grid, cir_item, cir_utils, cir_img, cir_timer, cir_mobile

pygame.init()


# Creating grid
grid = cir_grid.Grid()

# Loading images
images = cir_img.Images(grid)

# Creating my body item
if 1:
    my_body = cir_body.BodyItem(grid=grid, name="my body", color=grid.pink, speed=2)
    my_body.pos = grid.center_tile
    grid.items.append(my_body)

# Creating bokluk item
if 0:
    bokluk = cir_mobile.MobileItem(grid=grid, name="bokluk", color=grid.green, speed = 0)
    bokluk.pos = (grid.center_tile[0] + grid.cathetus, grid.center_tile[1] - grid.tile_radius)
    grid.items.append(bokluk)

# Creating timer item
if 1:
    lifespan = cir_timer.TimerItem(duration=30, time_color=grid.ungrey , grid=grid, name="test timer", color=grid.pink, speed=1)
    lifespan.pos = my_body.pos
    # TODO: make grid.timers list attribute
    grid.items.append(lifespan)




# TODO: Generate items and load from external file
mode_vs_options = {
    "my body": [
        cir_item.Item(grid=grid, name="option 1", color=my_body.default_color),
        cir_item.Item(grid=grid, name="option 2", color=my_body.default_color),
        cir_item.Item(grid=grid, name="option 3", color=my_body.default_color),
        cir_item.Item(grid=grid, name="move", color=my_body.default_color, image=images.feet),
        cir_item.Item(grid=grid, name="option 5", color=my_body.default_color),
        cir_item.Item(grid=grid, name="sensory", color=grid.azure, image=images.brain),
    ],
    "move" : [
        cir_item.Item(grid=grid, name="north", border=1, image=images.north),
        cir_item.Item(grid=grid, name="northeast", border=1, image=images.northeast),
        cir_item.Item(grid=grid, name="southeast", border=1, image=images.southeast),
        cir_item.Item(grid=grid, name="south", border=1, image=images.south),
        cir_item.Item(grid=grid, name="southwest", border=1, image=images.southwest),
        cir_item.Item(grid=grid, name="northwest", border=1, image=images.northwest)
    ],
    "sensory": [
        cir_item.Item(grid=grid, name="eat", color=grid.azure, image=images.lips_y),
        cir_item.Item(grid=grid, name="audio", color=grid.azure, image=images.ear_y),
        cir_item.Item(grid=grid, name="smel", color=grid.azure, image=images.nose_y),
        cir_item.Item(grid=grid, name="medi", color=grid.azure, image=images.yoga),
        cir_item.Item(grid=grid, name="touch", color=grid.azure, image=images.touch_y),
        cir_item.Item(grid=grid, name="see", color=grid.azure, image=images.eye_y)
    ],
    "bokluk": [
        cir_item.Item(grid=grid, name="govna", color=grid.black),
        cir_item.Item(grid=grid, name="laina", color=grid.green),
        cir_item.Item(grid=grid, name="otvrat", color=grid.green),
        cir_item.Item(grid=grid, name="smrad", color=grid.green),
        cir_item.Item(grid=grid, name="gadost", color=grid.green),
        cir_item.Item(grid=grid, name="gnus", color=grid.green)
    ],
    "govna": [
        cir_item.Item(grid=grid, name="shuplesto", color=grid.blue),
        cir_item.Item(grid=grid, name="luskavo", color=grid.blue),
        cir_item.Item(grid=grid, name="cherno", color=grid.black),
        cir_item.Item(grid=grid, name="mirizlivo", color=grid.blue),
        cir_item.Item(grid=grid, name="techno", color=grid.blue),
        cir_item.Item(grid=grid, name="mazno", color=grid.blue)
    ]
}

# Setting mode options
grid.set_mode_vs_options(mode_vs_options)


# GAME SETTINGS
gameDisplay = pygame.display.set_mode((grid.display_width, grid.display_height))
pygame.display.set_caption(grid.caption)
clock = pygame.time.Clock()
pygame.mouse.set_visible(True)




def seconds_in_game(START_TIME):
    """ Counts the seconds in the game """
    if time.time() > (START_TIME + grid.seconds_in_game):
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


def draw_item_options(item):
    """ Draws the item menu options """
    # TODO: menu background
    # pygame.draw.circle(gameDisplay, item.color, item.pos, grid.tile_radius * 3, 0)
    for option in item.options:
        if option.color:
            pygame.draw.circle(gameDisplay, option.color, option.pos, grid.tile_radius, option.border)
        if option.img:
            gameDisplay.blit(option.img, option.set_img_pos())


def draw_grid():
    """ Shows the grid tiles in white """
    for tile in grid.tiles:
        pygame.draw.circle(gameDisplay, grid.ungrey, tile, grid.tile_radius, 1)


def draw_movement(item):
    """ Shows the movement in cyan and the correct track in red """
    pygame.draw.line(gameDisplay, grid.red, item.move_track[0], item.move_track[-1], 1)
    for o in item.move_track:
        pygame.draw.circle(gameDisplay, grid.azure, o, 2, 1)


def draw_playing_tiles():
    """ Shows all tiles of the playing board in yellow """
    # TODO: define different playing board
    # TODO: show limits of the playing board
    for tile in grid.playing_tiles:
        pygame.draw.circle(gameDisplay, grid.gelb, tile, grid.tile_radius, 1)

def debug_print(mouse_pos, clicked_circle):
    print(""">>>>>> click: {0}, tile: {1}
mode        : {2}
menu        : {3}
grid items  : {4}
occupado:   : {5}
playing     : {6}
move track  : {7}
all tiles   : {8}
speed       : {9}
""".format(mouse_pos,
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


def game_loop():
    """    Main game loop.    """
    if grid.full_screen:
        pygame.display.toggle_fullscreen()

    GAME_EXIT = False
    START_TIME = time.time()


    while not GAME_EXIT:
        mouse_pos = pygame.mouse.get_pos()


        # lifespan timer
        lifespan.start_timer()

        # Timer - seconds in game
        seconds_in_game(START_TIME)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GAME_EXIT = True

            if event.type == pygame.KEYDOWN:
                # ========================================= ESCAPE LOOP ============================================= #
                if event.key is pygame.K_ESCAPE:
                    # TODO: K_ESCAPE screen loop here
                    # Restart
                    # os.execv(sys.executable, [sys.executable] + sys.argv)
                    GAME_EXIT = True

                # ========================================= ESCAPE LOOP ============================================= #

                # ========================================= SPACE BAR EVENTS ======================================== #
                if event.key == pygame.K_SPACE:
                    # Radar track populating
                    if not my_body.move_track and not my_body.in_menu and not my_body.radar_track:
                        my_body.gen_radar_track()
                        print ">>>> space"
                        print "revealed tiles: {0}".format(len(grid.revealed_tiles))
                        print "revealed_radius: {0}".format(len(grid.revealed_radius))
                # ========================================= SPACE BAR EVENTS ======================================== #


                # ========================================= MOVEMENT ================================================ #
                direction = None
                move_options = mode_vs_options["move"]
                arrows = [pygame.K_w, pygame.K_e, pygame.K_d, pygame.K_s, pygame.K_a, pygame.K_q]
                for idx, dir in enumerate(arrows):
                    if event.key is dir:
                        direction = move_options[idx].name
                if direction and not my_body.move_track and not my_body.radar_track:
                    my_body.gen_move_track(direction, move_options)
                # ========================================= MOVEMENT ================================================ #


            # ============================================= CLICK EVENTS ============================================ #
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_circle = grid.mouse_in_tile(mouse_pos)
                if clicked_circle:
                    for item in grid.items:
                        # Set in_menu for the items with menu (my_body)
                        item.check_in_menu(clicked_circle, mode_vs_options)
                        # Setting option positions
                        item.set_option_pos()
                        # ---------------------------------- Option clicked ----------------------------------------- #
                        if item.in_menu:
                            if item.options:
                                for option in item.options:
                                    if clicked_circle == option.pos:

                                        # If default option -> set mode
                                        if option in item.default_options:
                                            item.set_mode(option, mode_vs_options)

                                        # Check option specifics
                                        elif option in mode_vs_options[item.mode]:

                                            if item.mode is "move":
                                                item.gen_move_track(option.name, mode_vs_options[item.mode])

                                            elif option.name is "see":
                                                item.range += 1
                                                # item.mode = "seen"

                                            elif option.name is "smel":
                                                item.change_speed(1)

                                            elif option.name is "medi":
                                                item.range += 10

                                            elif option.name is "audio":
                                                item.change_speed(10)

                                            elif option.name is "eat":
                                                item.change_speed(-1)
                                            # Close menu if option selected
                                            item.set_in_menu(False)
                        # ---------------------------------- Option clicked ----------------------------------------- #

                debug_print(mouse_pos, clicked_circle)
            # ============================================= CLICK EVENTS ============================================ #

        # ================================================= DRAWING ================================================ #
        # -------------------------------------- Background -------------------------------------- #
        # Background
        gameDisplay.fill(grid.grey)

        # Revealed radius
        if grid.revealed_radius:
            draw_revealed_radius()

        # Grid
        if grid.show_grid:
            draw_grid()

        # Playing board:
        if grid.show_playing_tiles:
            draw_playing_tiles()
        # -------------------------------------- Background -------------------------------------- #

        # -------------------------------------- Animations -------------------------------------- #
        for item in grid.items:

            # Radar
            if item.radar_track:
                draw_radar(item)

            # Item options
            if item.in_menu:
                draw_item_options(item)

            # Body
            if (item.pos in grid.revealed_tiles) or (item is my_body):
                pygame.draw.circle(gameDisplay, item.color, item.pos, grid.tile_radius, item.border)
                if item.img:
                    gameDisplay.blit(item.img, item.set_img_pos())

            # Timer lifespan
            if item is lifespan:
                pygame.draw.circle(gameDisplay, item.color, item.pos, grid.tile_radius, 0)
                pygame.draw.arc(gameDisplay, item.time_color, item.rect, item.filled_angle, item.start_point, 5)

            # Show movement track in color
            if grid.show_movement and len(item.move_track) > 1:
                draw_movement(item)

        # Mouse Item
        # TODO: Create MouseItem
        # pygame.draw.circle(gameDisplay, grid.white, mouse_pos, 2, 0)
        for tile in grid.tiles:
            if cir_utils.in_circle(tile, grid.tile_radius, mouse_pos):
                pygame.draw.circle(gameDisplay, grid.white, tile, grid.tile_radius + 1, 1)
        # -------------------------------------- Animations -------------------------------------- #
        # ================================================== DRAWING ================================================ #

        pygame.display.update()

        # ================================================ CHANGE VARS ============================================== #
        for item in grid.items:
            # Movement
            if item.move_track:
                item.move()

        # Lifespan over
        if lifespan.is_over:
            GAME_EXIT = True

        # FPS
        clock.tick(grid.fps)
        # ================================================ CHANGE VARS ============================================== #
    pygame.quit()
    quit()

if __name__ == '__main__':
    game_loop()
