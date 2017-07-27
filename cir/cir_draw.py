#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                                    Drawing                                          #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
import cir_utils
import math


def set_img_pos(item_pos, grid):
    """
    Centers the image posotion
    :param grid:  grid object
    :return: coordinates of the centered image
    """
    img_x = item_pos[0] - grid.tile_radius
    img_y = item_pos[1] - grid.tile_radius
    return (img_x, img_y)


def set_emoji_pos(item_pos, grid):
    """
    Centers the emoji image posotion
    :param grid:  grid object
    :return: coordinates of the centered image
    """
    img_x = item_pos[0] - grid.tile_radius / 2
    img_y = item_pos[1] - grid.tile_radius / 2
    return (img_x, img_y)


def draw_background(grid):
    grid.game_display.fill(grid.fog_color)


def draw_hover(pygame, grid, MOUSE_POS, tile):
    """ Highlights the hovered tile """

    if cir_utils.in_circle(tile, grid.tile_radius, MOUSE_POS):
        pygame.draw.circle(grid.game_display,
                           grid.white,
                           tile,
                           grid.tile_radius,
                           1)


def draw_img(grid, item):
    """ Blit image on display """

    if item.img and item.available:
        if item.img.get_width() == grid.tile_radius:
            grid.game_display.blit(item.img, set_emoji_pos(item.pos, grid))
        else:
            grid.game_display.blit(item.img, set_img_pos(item.pos, grid))


def draw_radar(pygame, grid, item):
    """ Radar animation """

    radar_radius, thick = item.radar(grid)
    if radar_radius and thick:
        pygame.draw.circle(grid.game_display,
                           grid.white,
                           item.pos,
                           int(radar_radius),
                           int(thick))


def draw_revealed_radius(pygame, grid):
    """ Drawing the revealed areas (radius) """
    for revealed in grid.revealed_radius:
        pygame.draw.circle(grid.game_display,
                           grid.room_color,
                           revealed[0],
                           int(revealed[1]),
                           0)
        printed = revealed
        if printed:
            for to_be_printed in grid.revealed_radius:
                if printed[0] == to_be_printed[0]:
                    if printed[1] < to_be_printed[1]:
                        if printed in grid.revealed_radius:
                            grid.revealed_radius.remove(printed)


def draw_item_options(pygame, grid, MOUSE_POS, item):
    """ Draws the item menu options """

    for option in item.options:
        if option.available:
            if option.color:
                pygame.draw.circle(grid.game_display,
                                   option.color,
                                   option.pos,
                                   grid.tile_radius,
                                   option.border)
            if option.border_color:
                border_color = option.border_color
            else:
                border_color = grid.room_color
            pygame.draw.circle(grid.game_display,
                               border_color,
                               option.pos,
                               grid.tile_radius,
                               option.border_width)

            if option.img:
                draw_img(grid, option)
            draw_hover(pygame, grid, MOUSE_POS, option.pos)


def draw_menu_buttons(pygame, grid, MOUSE_POS):
    """ Drawing the buttons in the game menu """

    # Background
    draw_background(grid)

    # Buttons
    for button in grid.buttons:
        if button.available:
            if button.color:
                pygame.draw.circle(grid.game_display,
                                   button.color,
                                   button.pos,
                                   grid.tile_radius,
                                   button.border)
            if button.img:
                draw_img(grid, button)
            if button.text:
                grid.game_display.blit(button.text, button.text_rect)
            draw_hover(pygame, grid, MOUSE_POS, button.pos)


def draw_birth(grid, pygame, item):
    """ Draws the birth of an item """
    if item.birth_track:
        birth_step = item.birth_track[0]
        pygame.draw.circle(grid.game_display,
                           item.color,
                           item.pos,
                           birth_step,
                           0)


def draw_body(pygame, grid, MOUSE_POS, item):
    """ Draws each body and it's image if available """
    # for item in grid.bodies:
    if item.available and not item.birth_track:
        if item.color:
            pygame.draw.circle(grid.game_display,
                               item.color,
                               item.pos,
                               grid.tile_radius,
                               item.border)
        if item.img:
            draw_img(grid, item)
        draw_hover(pygame, grid, MOUSE_POS, item.pos)


def draw_timers(pygame, grid, item):
    """ Draws current state of a timer """
    if item.lifespan:
        if item.lifespan.available and item.time_color:
            item.lifespan.pos = item.pos
            pygame.draw.arc(grid.game_display,
                            item.time_color,
                            item.lifespan.rect,
                            math.radians(item.lifespan.filled_degrees),
                            math.radians(item.lifespan.start_degrees),
                            2)


def draw_grid(pygame, grid):
    """ Shows the grid tiles in white """
    for tile in grid.tiles:
        pygame.draw.circle(grid.game_display,
                           grid.room_color,
                           tile,
                           grid.tile_radius,
                           1)
    draw_playing_tiles(pygame, grid)


def draw_mask(pygame, grid):
    """ Draws the mas around the playing board """
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

    pygame.draw.rect(grid.game_display, grid.fog_color, rect1, 0)
    pygame.draw.rect(grid.game_display, grid.fog_color, rect2, 0)
    pygame.draw.polygon(grid.game_display, grid.fog_color, tri1, 0)
    pygame.draw.polygon(grid.game_display, grid.fog_color, tri2, 0)
    pygame.draw.polygon(grid.game_display, grid.fog_color, tri3, 0)
    pygame.draw.polygon(grid.game_display, grid.fog_color, tri4, 0)


def draw_mouse_image(pygame, grid, MOUSE_POS):
    """ Draws the Mouse image"""
    current_tile = grid.mouse_in_tile(MOUSE_POS)
    if current_tile and grid.mouse_img:
        pygame.draw.circle(grid.game_display,
                           grid.white,
                           current_tile,
                           grid.tile_radius,
                           1)
        if grid.mouse_img.get_width() == grid.tile_radius:
            grid.game_display.blit(grid.mouse_img, set_emoji_pos(current_tile, grid))
        else:
            grid.game_display.blit(grid.mouse_img, set_img_pos(current_tile, grid))


def draw_movement(pygame, grid, item):
    """ DEBUG: Shows the movement in cyan and the correct track in red """
    for move_step in item.move_track:
        pygame.draw.circle(grid.game_display,
                           grid.white,
                           move_step,
                           2,
                           1)


def draw_playing_tiles(pygame, grid):
    """ Shows all tiles of the playing board in yellow """
    if grid.playing_tiles:
        for tile in grid.playing_tiles:
            pygame.draw.circle(grid.game_display,
                               grid.gelb, tile,
                               grid.tile_radius,
                               1)



# --------------------------------------------------------------- #
#                                                                 #
#                           BACKGROUND                            #
#                                                                 #
# --------------------------------------------------------------- #
def draw_background_stuff(pygame, grid):
    """ Drawing deeper level background stuff """

    # Background
    draw_background(grid)

    # Revealed radius
    if grid.revealed_radius:
        draw_revealed_radius(pygame, grid)

    # Mask
    draw_mask(pygame, grid)

    # Grid
    if grid.show_grid:
        draw_grid(pygame, grid)

    # Playing board:
    if grid.show_playing_tiles:
        draw_playing_tiles(pygame, grid)


# --------------------------------------------------------------- #
#                                                                 #
#                           ANIMATIONS                            #
#                                                                 #
# --------------------------------------------------------------- #
def draw_animations(pygame, grid, MOUSE_POS):
    """ Main drawing function """
    # TEST PLACE


    # pygame.draw.lines(grid.game_display,
    #                   grid.dark_grey,
    #                   False,
    #                   [(693, 450), (795, 510)],
    #                   grid.tile_radius * 2)


    for item in grid.items:
        if item.available:

            # Birth
            draw_birth(grid, pygame, item)

            # Radar
            if item.radar_track:
                draw_radar(pygame, grid, item)

            # Items
            draw_body(pygame, grid, MOUSE_POS, item)

            # Show movement track in color
            if grid.show_movement and len(item.move_track) > 1:
                draw_movement(pygame, grid, item)

            # Image rotation
            if item.rot_track:
                item.rotate(pygame)

            # Item reverse rotation
            if item.last_rotation and not item.move_track and not item.direction:
                item.rotate_reverse(pygame)

            # Timers
            draw_timers(pygame, grid, item)

    # Item options
    for item in grid.items:
        if item.available:
            if item.in_menu:
                draw_item_options(pygame, grid, MOUSE_POS, item)

    # Mouse
    if grid.mouse_mode:
        draw_mouse_image(pygame, grid, MOUSE_POS)
