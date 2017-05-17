#######################################################################################################################
#################                                                                                     #################
#################                                    Drawing                                          #################
#################                                                                                     #################
#######################################################################################################################
import cir_utils


def draw_radar(pygame, grid, item):
    """ Radar animation """
    radar_radius, thick = item.radar()
    if radar_radius and thick:
        pygame.draw.circle(grid.game_display, item.grid.white, item.pos, radar_radius, thick)


def draw_revealed_radius(pygame, grid):
    """ Drawing the revealed areas """
    for revealed in grid.revealed_radius:
        pygame.draw.circle(grid.game_display, grid.ungrey, revealed[0], revealed[1], 0)
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
            grid.game_display.blit(option.img, option.set_img_pos())
        draw_hover(pygame, grid, MOUSE_POS, option.pos)


def draw_menu_buttons(pygame, grid, MOUSE_POS):
    """ Drawing the buttons in the game menu """

    for button in grid.buttons:
        if button.color:
            pygame.draw.circle(grid.game_display, button.color, button.pos, grid.tile_radius, button.border)
        if button.img:
            grid.game_display.blit(button.img, button.set_img_pos())
        if button.text:
            grid.game_display.blit(button.text, button.text_rect)
        draw_hover(pygame, grid, MOUSE_POS, button.pos)


def draw_body(pygame, grid, MOUSE_POS, item):
    """ Draws each body and it's image if available """
    pygame.draw.circle(grid.game_display, item.color, item.pos, grid.tile_radius, item.border)
    if item.img:
        grid.game_display.blit(item.img, item.set_img_pos())
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
        pygame.draw.circle(grid.game_display, grid.ungrey, tile, grid.tile_radius, 1)
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

    pygame.draw.rect(grid.game_display, grid.grey, rect1, 0)
    pygame.draw.rect(grid.game_display, grid.grey, rect2, 0)
    pygame.draw.polygon(grid.game_display, grid.grey, tri1, 0)
    pygame.draw.polygon(grid.game_display, grid.grey, tri2, 0)

    pygame.draw.polygon(grid.game_display, grid.grey, tri3, 0)
    pygame.draw.polygon(grid.game_display, grid.grey, tri4, 0)


def draw_hover(pygame, grid, MOUSE_POS, tile):
    """ Highlights the hovered tile """
    if cir_utils.in_circle(tile, grid.tile_radius, MOUSE_POS):
        pygame.draw.circle(grid.game_display, grid.white, tile, grid.tile_radius + 1, 2)


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