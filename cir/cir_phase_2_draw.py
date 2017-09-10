# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                     DRAW                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import cir_utils
import math


class GameDrawer(object):

    def __init__(self, grid=None):
        self.grid = grid
        # self.grid.pygame = pygame



    def set_img_pos(self, item_pos):
        """
        Centers the image posotion
        :param grid:  grid object
        :return: coordinates of the centered image
        """
        img_x = item_pos[0] - self.grid.tile_radius
        img_y = item_pos[1] - self.grid.tile_radius
        return (img_x, img_y)


    def set_emoji_pos(self, item_pos):
        """
        Centers the emoji image posotion
        :param grid:  grid object
        :return: coordinates of the centered image
        """
        img_x = item_pos[0] - self.grid.tile_radius / 2
        img_y = item_pos[1] - self.grid.tile_radius / 2
        return (img_x, img_y)

    def set_map_pos(self, item_pos):
        """
        Centers the emoji image posotion
        :param grid:  grid object
        :return: coordinates of the centered image
        """
        img_x = item_pos[0] - self.grid.tile_radius + 5
        img_y = item_pos[1] - self.grid.tile_radius
        return (img_x, img_y)


    def draw_background(self):
        self.grid.game_display.fill(self.grid.fog_color)


    def draw_hover(self, current_tile, item):
        """ Highlights the hovered tile """
        if current_tile:
            if cir_utils.in_circle(item.pos, self.grid.tile_radius, current_tile):
                if item.type == "map_tile" and not self.grid.mouse_mode:
                    radius = self.grid.tile_radius - 4
                else:
                    radius = self.grid.tile_radius
                self.grid.pygame.draw.circle(self.grid.game_display,
                                             self.grid.white,
                                             item.pos,
                                             radius,
                                             1)


    def draw_img(self, item):
        """ Blit image on display """

        if item.img and item.available and not item.birth_track:

            if item.img.get_width() == self.grid.tile_radius:
                self.grid.game_display.blit(item.img, self.set_emoji_pos(item.pos))
            elif item.img.get_width() == (self.grid.tile_radius * 2) - 10:
                self.grid.game_display.blit(item.img, self.set_map_pos(item.pos))
            else:
                self.grid.game_display.blit(item.img, self.set_img_pos(item.pos))


    def draw_radar(self, item):
        """ Radar animation """
        radar_radius, thick = item.radar(self.grid)

        if item.color:
            wave_color = item.color
        else:
            wave_color = self.grid.white

        if radar_radius and thick:
            self.grid.pygame.draw.circle(self.grid.game_display,
                               wave_color,
                               item.pos,
                               int(radar_radius),
                               int(thick))


    def draw_revealed_radius(self):
        """ Drawing the revealed areas (radius) """
        for revealed in self.grid.revealed_radius:
            self.grid.pygame.draw.circle(self.grid.game_display,
                               self.grid.room_color,
                               revealed[0],
                               int(revealed[1]),
                               0)
            drawn = revealed
            if drawn:
                for to_be_drawn in self.grid.revealed_radius:
                    if drawn[0] == to_be_drawn[0]:
                        if drawn[1] < to_be_drawn[1]:
                            if drawn in self.grid.revealed_radius:
                                self.grid.revealed_radius.remove(drawn)


    def draw_menu_buttons(self, current_tile):
        """ Drawing the buttons in the game menu """

        # Background
        self.draw_background()

        # Buttons
        for button in self.grid.buttons:
            if button.available:
                if button.color:
                    self.grid.pygame.draw.circle(self.grid.game_display,
                                       button.color,
                                       button.pos,
                                       self.grid.tile_radius,
                                       0)
                if button.img:
                    self.draw_img(button)
                if button.text:
                    self.grid.game_display.blit(button.text, button.text_rect)
                self.draw_hover(current_tile, button)


    def draw_body(self, current_tile, item):
        """ Draws each body and it's image if available """

        if item.available:
            blit_item = True

            if item.birth_track:
                item.radius = item.birth_track[0]
            elif not item.birth_track and item.fat_track:
                item.radius = item.fat_track[0]
            if not item.birth_track and item.marked_for_destruction:
                blit_item = False


            if blit_item:
                if item.color:
                    self.grid.pygame.draw.circle(self.grid.game_display,
                                       item.color,
                                       item.pos,
                                       item.radius,
                                       0)
                if item.category == "bag":
                    self.grid.pygame.draw.circle(self.grid.game_display,
                                                 self.grid.yellow,
                                                 item.pos,
                                                 self.grid.tile_radius,
                                                 1)
                # Draw activation / deactivation here

                self.draw_img(item)
                self.draw_aim(current_tile, item)
                self.draw_hover(current_tile, item)

    def draw_timers(self, item):
        """ Draws current state of a timer """
        if item.lifespan:
            timer_fat = item.radius / 5

            if item.lifespan.available and item.time_color:
                if item.radius >= timer_fat:
                    item.lifespan.pos = item.pos
                    item.lifespan.radius = item.radius
                    self.grid.pygame.draw.arc(self.grid.game_display,
                                    item.time_color,
                                    item.lifespan.rect,
                                    math.radians(item.lifespan.filled_degrees),
                                    math.radians(item.lifespan.start_degrees),
                                    timer_fat)

    def draw_aim(self, current_tile, item):
        """ Aim """
        if item.mode == "echo" and item.available:
            aim_dir_idx = item.get_aiming_direction(self.grid, current_tile)[1]
            # aim_tile = item.get_aiming_direction(self.grid, current_tile)[0]

            aim_fat  = item.radius / 5
            aim_dist = aim_fat
            aim_rect = [item.rect[0] - aim_dist,
                        item.rect[1] - aim_dist,
                        item.rect[2] + aim_dist * 2,
                        item.rect[3] + aim_dist * 2]
            if item.color:
                aim_color = item.color
            else:
                aim_color = self.grid.white

            angle1, angle2 = None, None
            if aim_dir_idx == 0:
                angle1, angle2 = 60, 120
            elif aim_dir_idx == 1:
                angle1, angle2 = 360, 60
            elif aim_dir_idx == 2:
                angle1, angle2 = 300, 360
            elif aim_dir_idx == 3:
                angle1, angle2 = 240, 300
            elif aim_dir_idx == 4:
                angle1, angle2 = 180, 240
            elif aim_dir_idx == 5:
                angle1, angle2 = 120, 180

            if angle1 and angle2 and item.radius >= aim_fat:
                self.grid.pygame.draw.arc(self.grid.game_display,
                                aim_color,
                                aim_rect,
                                math.radians(angle1),
                                math.radians(angle2),
                                aim_fat)

    def draw_grid(self):
        """ Shows the grid tiles in white """
        for tile in self.grid.tiles:
            self.grid.pygame.draw.circle(self.grid.game_display,
                               self.grid.room_color,
                               tile,
                               self.grid.tile_radius,
                               1)

        self.draw_playing_tiles()


    def draw_tile_names(self):
        for tile_name, tile_centre in self.grid.tile_dict.items():
            font = getattr(self.grid.fonts, 'tiny')
            text = font.render(str(tile_name), True, self.grid.white)
            rect = text.get_rect()
            rect.center = tile_centre
            self.grid.game_display.blit(text, rect)


    def draw_mask(self):
        """ Draws the mas around the playing board """
        if self.grid.cols == 24 and self.grid.rows == 24:
            rect1 = [
                (0,0),
                (self.grid.center_tile[0] - ((4 * self.grid.cathetus) + (self.grid.cathetus / 2) + 5), (self.grid.display_height))
                    ]
            rect2 = [
                (self.grid.center_tile[0] + ((4 * self.grid.cathetus) + (self.grid.cathetus / 2) + 5), 0),
                (self.grid.center_tile[0], self.grid.display_height)
                    ]
            tri1 = [
                (self.grid.center_tile[0] - ((4 * self.grid.cathetus) + (self.grid.cathetus / 2) + 5), (self.grid.center_tile[0] - 13 * self.grid.tile_radius)),
                (self.grid.center_tile[0] - ((4 * self.grid.cathetus) + (self.grid.cathetus / 2) + 5), 0),
                (self.grid.center_tile[0] + ((2 * self.grid.cathetus) + (self.grid.cathetus / 2) + 0), 0)
            ]
            tri2 = [
                (self.grid.center_tile[0] + ((4 * self.grid.cathetus) + (self.grid.cathetus / 2) + 5), (self.grid.center_tile[0] - 14 * self.grid.tile_radius)),
                (self.grid.center_tile[0] + ((4 * self.grid.cathetus) + (self.grid.cathetus / 2) + 5), 0),
                (self.grid.center_tile[0] - ((2 * self.grid.cathetus) + (self.grid.cathetus / 2) + 5), 0)
            ]
            tri3 = [
                (self.grid.center_tile[0] - ((4 * self.grid.cathetus) + (self.grid.cathetus / 2) + 5), (self.grid.center_tile[0] - 5 * self.grid.tile_radius)),
                (self.grid.center_tile[0] - ((4 * self.grid.cathetus) + (self.grid.cathetus / 2) + 5), self.grid.display_height),
                (self.grid.center_tile[0] + ((2 * self.grid.cathetus) + (self.grid.cathetus / 2) + 5), self.grid.display_height)
            ]
            tri4 = [
                (self.grid.center_tile[0] + ((4 * self.grid.cathetus) + (self.grid.cathetus / 2) + 5), (self.grid.center_tile[0] - 5 * self.grid.tile_radius)),
                (self.grid.center_tile[0] + ((4 * self.grid.cathetus) + (self.grid.cathetus / 2) + 5), self.grid.display_height),
                (self.grid.center_tile[0] - ((2 * self.grid.cathetus) + (self.grid.cathetus / 2) + 5), self.grid.display_height)
            ]

            self.grid.pygame.draw.rect(self.grid.game_display, self.grid.fog_color, rect1, 0)
            self.grid.pygame.draw.rect(self.grid.game_display, self.grid.fog_color, rect2, 0)
            self.grid.pygame.draw.polygon(self.grid.game_display, self.grid.white, tri1, 0)
            self.grid.pygame.draw.polygon(self.grid.game_display, self.grid.red, tri2, 0)
            self.grid.pygame.draw.polygon(self.grid.game_display, self.grid.fog_color, tri3, 0)
            self.grid.pygame.draw.polygon(self.grid.game_display, self.grid.fog_color, tri4, 0)
        else:

            points = self.grid.names_to_pos(["11_1", "16_6", "16_16", "11_21", "6_16", "6_6"])
            self.grid.pygame.draw.lines(self.grid.game_display, self.grid.red, True, points, 50)

            fat = int((4 * self.grid.tile_radius) + (4.5 * self.grid.cathetus))

            rec1 = self.grid.names_to_pos(["19_1", "19_21"])
            self.grid.pygame.draw.lines(self.grid.game_display, self.grid.red, True, rec1, fat)
            rec2 = self.grid.names_to_pos(["3_1", "3_21"])
            self.grid.pygame.draw.lines(self.grid.game_display, self.grid.red, True, rec2, fat)
            tri1 = self.grid.names_to_pos(["13_1", "17_1", "17_5"])
            self.grid.pygame.draw.lines(self.grid.game_display, self.grid.red, True, tri1, 3 * self.grid.tile_radius)
            lin1 = self.grid.names_to_pos(["1_1", "21_1"])
            self.grid.pygame.draw.lines(self.grid.game_display, self.grid.red, True, lin1, 2 * self.grid.tile_radius)

            lin2 = self.grid.names_to_pos(["1_21", "21_21"])
            self.grid.pygame.draw.lines(self.grid.game_display, self.grid.red, True, lin2, 2 * self.grid.tile_radius)

    def draw_mouse_image(self, current_tile):
        """ Draws the Mouse image"""
        if current_tile and self.grid.mouse_img:
            self.grid.pygame.draw.circle(self.grid.game_display,
                               self.grid.yellow,
                               current_tile,
                               self.grid.tile_radius,
                               1)
            if self.grid.mouse_img.get_width() == self.grid.tile_radius:
                self.grid.game_display.blit(self.grid.mouse_img, self.set_emoji_pos(current_tile))
            else:
                self.grid.game_display.blit(self.grid.mouse_img, self.set_img_pos(current_tile))


    def draw_movement(self, item):
        """ DEBUG: Shows the movement in cyan and the correct track in red """
        for move_step in item.move_track:
            self.grid.pygame.draw.circle(self.grid.game_display,
                               self.grid.white,
                               move_step,
                               2,
                               1)


    def draw_playing_tiles(self):
        """ Shows all tiles of the playing board in yellow """
        if self.grid.playing_tiles:
            for tile in self.grid.playing_tiles:
                self.grid.pygame.draw.circle(self.grid.game_display,
                                   self.grid.gelb, tile,
                                   self.grid.tile_radius,
                                   1)



    # --------------------------------------------------------------- #
    #                                                                 #
    #                           BACKGROUND                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    def draw_background_stuff(self):
        """ Drawing deeper level background stuff """

        # Background
        self.draw_background()

        # Revealed radius
        if self.grid.revealed_radius:
            self.draw_revealed_radius()

        # Mask
        self.draw_mask()

        # Grid
        if self.grid.show_grid:
            self.draw_grid()

        # Playing board:
        if self.grid.show_playing_tiles:
            self.draw_playing_tiles()






    # --------------------------------------------------------------- #
    #                                                                 #
    #                           ANIMATIONS                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    def draw_animations(self, current_tile):
        """ Main drawing function """
        # TEST PLACE

        # self.grid.pygame.draw.lines(grid.game_display,
        #                   grid.dark_grey,
        #                   False,
        #                   [(693, 450), (795, 510)],
        #                   grid.tile_radius * 2)

        for item in self.grid.items:

            if item.available:

                # Radar
                if item.vibe_track:
                    self.draw_radar(item)

                # Items
                self.draw_body(current_tile, item)

                # Show movement track in color
                if self.grid.show_movement and len(item.move_track) > 1:
                    self.draw_movement(item)

                # Image rotation
                if item.rot_track:
                    item.rotate(self.grid.pygame)

                # Item reverse rotation
                if item.last_rotation and not item.move_track and not item.direction:
                    item.rotate_reverse(self.grid.pygame)

                # Timers
                self.draw_timers(item)


        # Mouse
        if self.grid.mouse_mode:
            self.draw_mouse_image(current_tile)

        # Tile names
        if self.grid.show_tile_names:
            self.draw_grid()
            self.draw_tile_names()

    def draw(self, current_tile):
        """
        Draws everything
        :param current_tile: coordinates of current tile
        """
        # BACKGROUND
        self.draw_background_stuff()
        # ANIMATIONS
        self.draw_animations(current_tile)
        # UPDATE
        self.grid.pygame.display.update()