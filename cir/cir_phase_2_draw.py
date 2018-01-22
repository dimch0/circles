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


    def draw_map(self):
        "draws map dots"
        for map_dot in self.grid.map_dots.values():
            self.grid.pygame.draw.circle(self.grid.game_display,
                                         map_dot['color'],
                                         map_dot['pos'],
                                         map_dot['radius'],
                                         0)


    def draw_hover(self, current_tile, item):
        """ Highlights the hovered tile """
        if current_tile and not item.type in ["door", "door_enter"]:
            if cir_utils.in_circle(item.pos, self.grid.tile_radius, current_tile):
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
            elif item.type in ['door_enter']:
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


    def draw_menu_buttons(self, current_tile):
        """ Drawing the buttons in the game menu """

        # Background
        self.grid.game_display.fill(self.grid.fog_color)
        self.draw_msg()

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
                if hasattr(button, 'text'):
                    if button.text:
                        self.grid.game_display.blit(button.text, button.text_rect)
                self.draw_hover(current_tile, button)




    def draw_body(self, current_tile, item):
        """ Draws each body and it's image if available """

        if item.available and not (not item.birth_track and item.marked_for_destruction) and item.pos:

            if item.birth_track and item.color:
                item.radius = item.birth_track[0]

            if item.color:
                self.grid.pygame.draw.circle(self.grid.game_display,
                                   item.color,
                                   item.pos,
                                   item.radius,
                                   0)

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
            self.draw_hover(current_tile, item)

    def draw_timers(self, item):
        """ Draws current state of a timer """
        timer = None

        if hasattr(item, 'lifespan'):
            if item.lifespan not in ['', None]:
                timer = item.lifespan

        if not timer and hasattr(item, 'vfreq'):
            if item.vfreq:
                timer = item.vfreq

        if timer:
            timer_fat = 4

            if timer.available and item.time_color:
                if item.radius >= timer_fat:
                    timer.pos = item.pos
                    timer.radius = item.radius
                    self.grid.pygame.draw.arc(self.grid.game_display,
                                              item.time_color,
                                              timer.rect,
                                              math.radians(timer.filled_degrees),
                                              math.radians(timer.start_degrees),
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
            for idx, msg in enumerate(self.grid.messages[-self.grid.max_msg:]):
                msg = msg.replace("SCREEN - ", "")
                font = getattr(self.grid.fonts, 'small')
                if "+" in msg or "-" in msg:
                    color = self.grid.grey05
                elif msg in ['you loose', 'you dead']:
                    color = self.grid.red01
                elif msg in ['you win']:
                    color = self.grid.gelb05
                else:
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
    def draw_background(self):

        # BACKGROUND
        self.grid.game_display.fill(self.grid.fog_color)

        # REVEALED
        for rev_tile, rev_radius in self.grid.revealed_tiles.items():
            if rev_radius:
                rradius = rev_radius[0]
            else:
                rradius = self.grid.tile_radius

            self.grid.pygame.draw.circle(self.grid.game_display,
                                         self.grid.room_color,
                                         rev_tile,
                                         rradius,
                                         0)
            if rev_radius:
                rev_radius.pop(0)

        # MAP
        if self.grid.draw_map:
            self.draw_map()


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

        # MSG
        self.draw_msg()

    def draw(self, current_tile):
        """
        Draws everything
        :param current_tile: coordinates of current tile
        """
        # BACKGROUND
        self.draw_background()
        # ANIMATIONS
        self.draw_animations(current_tile)

        # UPDATE
        self.grid.pygame.display.update()