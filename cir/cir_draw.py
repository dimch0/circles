#######################################################################################################################
#################                                                                                     #################
#################                                    Drawing                                          #################
#################                                                                                     #################
#######################################################################################################################
import cir_utils
import pdb
from cir_item import Item


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


def draw_img(grid, item):
    if item.img:
        # pdb.set_trace()
        if item.img.get_width() == grid.tile_radius:
            grid.game_display.blit(item.img, set_emoji_pos(item.pos, grid))
            # print "Here"
        else:
            grid.game_display.blit(item.img, set_img_pos(item.pos, grid))

def draw_radar(pygame, grid, item):
    """ Radar animation """
    radar_radius, thick = item.radar()
    if radar_radius and thick:
        pygame.draw.circle(grid.game_display, item.grid.white, item.pos, radar_radius, thick)


def draw_revealed_radius(pygame, grid):
    """ Drawing the revealed areas """
    for revealed in grid.revealed_radius:
        pygame.draw.circle(grid.game_display, grid.grey, revealed[0], revealed[1], 0)
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
        if option.color:
            pygame.draw.circle(grid.game_display, option.color, option.pos, grid.tile_radius, option.border)
        if option.img:
            draw_img(grid, option)
            # grid.game_display.blit(option.img, Item.set_img_pos(option.pos, grid))
        draw_hover(pygame, grid, MOUSE_POS, option.pos)


def draw_menu_buttons(pygame, grid, MOUSE_POS):
    """ Drawing the buttons in the game menu """

    for button in grid.buttons:
        if button.color:
            pygame.draw.circle(grid.game_display, button.color, button.pos, grid.tile_radius, button.border)
        if button.img:
            draw_img(grid, button)
            # grid.game_display.blit(button.img, Item.set_img_pos(button.pos, grid))
        if button.text:
            grid.game_display.blit(button.text, button.text_rect)
        draw_hover(pygame, grid, MOUSE_POS, button.pos)


def draw_body(pygame, grid, MOUSE_POS, item):
    """ Draws each body and it's image if available """
    if item.color:
        pygame.draw.circle(grid.game_display, item.color, item.pos, grid.tile_radius, item.border)
    if item.img:
        draw_img(grid, item)
        # grid.game_display.blit(item.img, Item.set_img_pos(item.pos, grid))
    draw_hover(pygame, grid, MOUSE_POS, item.pos)


def draw_timers(pygame, grid, my_body):
    """ Draws current state of a timer """
    # pygame.draw.circle(grid.game_display, timer.color, timer.pos, grid.tile_radius, 0)
    for timer in grid.timers:
        if timer.name == "lifespan":
            timer.pos = my_body.pos
        pygame.draw.arc(grid.game_display, timer.time_color, timer.rect, timer.filled_angle, timer.start_point, 2)


def draw_grid(pygame, grid):
    """ Shows the grid tiles in white """
    for tile in grid.tiles:
        pygame.draw.circle(grid.game_display, grid.grey, tile, grid.tile_radius, 1)
    draw_playing_tiles(pygame, grid)


def draw_mask(pygame, grid):
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

    pygame.draw.rect(grid.game_display, grid.dark_grey, rect1, 0)
    pygame.draw.rect(grid.game_display, grid.dark_grey, rect2, 0)
    pygame.draw.polygon(grid.game_display, grid.dark_grey, tri1, 0)
    pygame.draw.polygon(grid.game_display, grid.dark_grey, tri2, 0)

    pygame.draw.polygon(grid.game_display, grid.dark_grey, tri3, 0)
    pygame.draw.polygon(grid.game_display, grid.dark_grey, tri4, 0)


def draw_hover(pygame, grid, MOUSE_POS, tile):
    """ Highlights the hovered tile """
    if cir_utils.in_circle(tile, grid.tile_radius, MOUSE_POS):
        pygame.draw.circle(grid.game_display, grid.white, tile, grid.tile_radius + 1, 2)


def draw_mouse_image(pygame, grid, MOUSE_POS):
    """ Draws the Mouse image"""
    current_tile = grid.mouse_in_tile(MOUSE_POS)
    if current_tile and grid.mouse_img:
        pygame.draw.circle(grid.game_display, grid.white, current_tile, grid.tile_radius + 1, 2)
        # TODO: Create a mouse item class
        grid.game_display.blit(grid.mouse_img, set_img_pos(current_tile, grid))



def draw_movement(pygame, grid, item):
    """ DEBUG: Shows the movement in cyan and the correct track in red """
    pygame.draw.line(grid.game_display, grid.azure, item.move_track[0], item.move_track[-1], 1)
    for o in item.move_track:
        pygame.draw.circle(grid.game_display, grid.white, o, 2, 1)


def draw_playing_tiles(pygame, grid):
    """ Shows all tiles of the playing board in yellow """
    if grid.playing_tiles:
        for tile in grid.playing_tiles:
            pygame.draw.circle(grid.game_display, grid.gelb, tile, grid.tile_radius, 1)