# -*- coding: utf-8 -*-
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

    def set_neon_pos(self, item_pos):
        """
        Centers the emoji image posotion
        :param grid:  grid object
        :return: coordinates of the centered image
        """
        img_x = item_pos[0] - self.grid.tile_radius * 1.25
        img_y = item_pos[1] - self.grid.tile_radius * 1.25
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
            elif item.img.get_width() == (self.grid.tile_radius - 5) * 2:
                self.grid.game_display.blit(item.img, self.set_map_pos(item.pos))
            elif item.type in ['sign', 'door_enter']:
                self.grid.game_display.blit(item.img, self.set_neon_pos(item.pos))
            else:
                self.grid.game_display.blit(item.img, self.set_img_pos(item.pos))


    def draw_vibe(self, item):
        """ Vibe animation """
        vibe_radius, thick = item.vibe_track[0]
        if item.color:
            vibe_color = item.color
        else:
            vibe_color = self.grid.white

        # if vibe_radius and thick:
        self.grid.pygame.draw.circle(self.grid.game_display,
                           vibe_color,
                           item.pos,
                           int(vibe_radius),
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

        if item.available and not (not item.birth_track and item.marked_for_destruction):

            if item.birth_track:
                item.radius = item.birth_track[0]

            if item.color:
                self.grid.pygame.draw.circle(self.grid.game_display,
                                   item.color,
                                   item.pos,
                                   item.radius,
                                   0)
            if item.category == "bag":
                self.grid.pygame.draw.circle(self.grid.game_display,
                                             self.grid.gelb05,
                                             item.pos,
                                             self.grid.tile_radius,
                                             1)

            # DRAW EFFECT ACTIVATION
            if item.effect_track:
                if item.default_color:
                    eff_cir = item.effect_track[0]
                    item.color = eff_cir["color"]
                    self.grid.pygame.draw.circle(self.grid.game_display,
                                                 item.default_color,
                                                 item.pos,
                                                 eff_cir["radius"])


            self.draw_img(item)
            self.draw_aim(current_tile, item)
            if not item.type in ['sign']:
                self.draw_hover(current_tile, item)

    def draw_timers(self, item):
        """ Draws current state of a timer """
        if item.lifespan:
            timer_fat = 2

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
        if self.grid.mouse_mode in ["echo"] and item.available and item.type in ['my_body']:
            aim_dir_idx = item.get_aiming_direction(self.grid, current_tile)[1]
            # aim_tile = item.get_aiming_direction(self.grid, current_tile)[0]

            aim_fat  = 2
            aim_dist = aim_fat * 3
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
        for tile_name, tile_centre in self.grid.tile_dict.items():

            self.grid.pygame.draw.circle(self.grid.game_display,
                                         self.grid.room_color,
                                         tile_centre,
                                         self.grid.tile_radius,
                                         1)


            font = getattr(self.grid.fonts, 'tiny')
            text = font.render(str(tile_name), True, self.grid.white)
            rect = text.get_rect()
            rect.center = tile_centre
            self.grid.game_display.blit(text, rect)


    def draw_mask(self):
        """ Draws the mas around the playing board """
        if self.grid.cols == 22 and self.grid.rows == 22:
            fat = int((4 * self.grid.tile_radius) + (4.5 * self.grid.cathetus))
            fat_tri = int(3 * self.grid.tile_radius) - 8

            point_lines = [
                {   "fat"   : 50,
                    "points": ["11_1", "16_6", "16_16", "11_21", "6_16", "6_6", "11_1"]},
                {   "fat"   : fat,
                    "points": ["19_1", "19_21"]},
                {   "fat"   : fat,
                    "points": ["3_1", "3_21"]},
                {   "fat"   : fat_tri,
                    "points": ["16_4", "13_1", "13_3"]},
                {   "fat"   : fat_tri,
                    "points": ["15_1", "16_2"]},
                {   "fat"   : fat_tri,
                    "points": ["13_3", "13_1", "16_4", "15_1"]},
                {   "fat"   : fat_tri,
                    "points": ["9_3", "9_1", "6_4", "7_1"]},
                {   "fat"   : fat_tri,
                    "points": ["9_19", "9_21", "6_18", "7_21"]},
                {   "fat"   : fat_tri,
                    "points": ["13_19", "13_21", "16_18", "15_21"]},
            ]

            for fig in point_lines:
                self.grid.pygame.draw.lines(self.grid.game_display,
                                            self.grid.fog_color,
                                            False,
                                            self.grid.names_to_pos(fig["points"]),
                                            fig["fat"])

            lin1 = [(0, 0), (self.grid.display_width, self.grid.display_height)]
            self.grid.pygame.draw.rect(self.grid.game_display, self.grid.fog_color, lin1, fat_tri)


    def draw_mouse_image(self, current_tile):
        """ Draws the Mouse image"""
        if current_tile and self.grid.mouse_img:
            self.grid.pygame.draw.circle(self.grid.game_display,
                               self.grid.white,
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
                               self.grid.cyan01,
                               move_step,
                               2,
                               1)


    def draw_msg(self):
        if self.grid.messages:
            for idx, msg in enumerate(self.grid.messages):
                font = getattr(self.grid.fonts, 'small')
                msg = msg.replace(u"SCREEN - ", u"")

                color = self.grid.white
                # if idx == 0:
                #     color = self.grid.white
                # else:
                #     color = self.grid.room_color

                msg = msg.lower()
                # msg = u"黒澤 明 €"
                txt = font.render(msg, True, color)

                txt_rect = self.grid.pygame.Rect(20, 59, 20, 100)
                # txt_rect.center = (self.grid.tile_dict["16_2"][0], 50 + (20 * idx))
                # txt_rect.center = (self.grid.tile_dict["17_7"][0], (7 * self.grid.tile_radius) + 18 + (18 * idx))
                txt_rect.center = (self.grid.tile_dict["0_2"][0], self.grid.tile_dict["0_2"][1] + (18 * idx))

                self.grid.game_display.blit(txt, txt_rect)

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


    # --------------------------------------------------------------- #
    #                                                                 #
    #                           ANIMATIONS                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    def draw_animations(self, current_tile):
        """ Main drawing function """

        for item in self.grid.items:

            if item.available:

                # VIBE
                if item.vibe_track:
                    self.draw_vibe(item)

                # ITEMS
                self.draw_body(current_tile, item)

                # SHOW MOVEMENT
                if self.grid.show_debug and len(item.move_track) > 1:
                    self.draw_movement(item)

                # TIMERS
                self.draw_timers(item)


        # MOUSE
        if self.grid.mouse_mode:
            self.draw_mouse_image(current_tile)

        # GRID
        if self.grid.show_grid:
            self.draw_grid()

    def draw(self, current_tile):
        """
        Draws everything
        :param current_tile: coordinates of current tile
        """
        # BACKGROUND
        self.draw_background_stuff()
        # ANIMATIONS
        self.draw_animations(current_tile)
        self.draw_msg()
        # UPDATE
        self.grid.pygame.display.update()