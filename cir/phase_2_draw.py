# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                     DRAW                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import grid_util
import math


class GameDrawer(object):

    def __init__(self, grid=None):
        self.grid = grid
        # self.grid.pygame = pygame


    def set_img_pos(self, center, image):
        """
        Centers the image posotion
        :param grid:  grid object
        :return: coordinates of the centered image
        """
        half_side = image.get_width() / 2
        img_x = center[0] - half_side
        img_y = center[1] - half_side
        return (img_x, img_y)

    def draw_map(self):
        "draws map dots"
        for map_dot in self.grid.map_dots.values():
            self.grid.pygame.draw.circle(self.grid.game_display,
                                         map_dot['color'],
                                         map_dot['pos'],
                                         map_dot['radius'],
                                         0)

    def draw_hover(self, current_tile, circle):
        """ Highlights the hovered tile """
        nohover = ["door", "door_enter"]
        if current_tile and not any(nohover in circle.type for nohover in nohover):
            if grid_util.in_circle(circle.pos, self.grid.tile_radius, current_tile):
                radius = self.grid.tile_radius
                self.grid.pygame.draw.circle(self.grid.game_display,
                                             self.grid.white,
                                             circle.pos,
                                             radius,
                                             1)

    def draw_img(self, circle):
        """ Blit image on display """
        if circle.img and circle.available and not circle.birth_track:
            self.grid.game_display.blit(circle.img, self.set_img_pos(circle.pos, circle.img))

    def draw_vibe(self, circle):
        """ Vibe animation """
        vibe_center = circle.vibe_track['center']
        vibe_radius, thick = circle.vibe_track['track'][0]
        if circle.color:
            vibe_color = circle.color
        else:
            vibe_color = self.grid.white

        # if vibe_radius and thick:
        self.grid.pygame.draw.circle(self.grid.game_display,
                           vibe_color,
                           vibe_center,
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




    def draw_body(self, current_tile, circle):
        """ Draws each body and it's image if available """

        if circle.available and not (not circle.birth_track and circle.marked_for_destruction) and circle.pos:

            if circle.birth_track and circle.color:
                circle.radius = circle.birth_track[0]

            border = 0
            if 'door' in circle.type:
                border = self.grid.tile_border

            if circle.radius < border:
                circle.radius = border
            if circle.color:
                self.grid.pygame.draw.circle(self.grid.game_display,
                                   circle.color,
                                   circle.pos,
                                   circle.radius,
                                   border)

            # DRAW EFFECT ACTIVATION
            if circle.effect_track:
                if circle.default_color:
                    eff_cir = circle.effect_track[0]
                    circle.color = eff_cir["color"]
                    self.grid.pygame.draw.circle(self.grid.game_display,
                                                 circle.default_color,
                                                 circle.pos,
                                                 eff_cir["radius"])
            self.draw_img(circle)
            self.draw_aim(current_tile, circle)
            self.draw_hover(current_tile, circle)

    def draw_timers(self, circle):
        """ Draws current state of a timer """
        pass
        # timer = None
        #
        # if hasattr(circle, 'lifespan'):
        #     if circle.lifespan not in ['', None]:
        #         timer = circle.lifespan
        #
        # if not timer and hasattr(circle, 'vfreq'):
        #     if circle.vfreq:
        #         timer = circle.vfreq
        #
        # if timer:
        #     timer_fat = 1
        #
        #     if timer.available and circle.time_color:
        #         if circle.radius >= timer_fat:
        #             timer.pos = circle.pos
        #             timer.radius = circle.radius
        #             self.grid.pygame.draw.arc(self.grid.game_display,
        #                                       circle.time_color,
        #                                       timer.rect,
        #                                       math.radians(timer.filled_degrees),
        #                                       math.radians(timer.start_degrees),
        #                                       timer_fat)

    def draw_aim(self, current_tile, circle):
        """ Aim """
        if self.grid.mouse_mode in ["echo"] and circle.available and "mybody" in circle.type:
            aim_dir_idx = circle.get_aiming_direction(self.grid, current_tile)[1]
            # aim_tile = circle.get_aiming_direction(self.grid, current_tile)[0]

            aim_fat  = 2
            aim_dist = aim_fat * 3
            aim_rect = [circle.rect[0] - aim_dist,
                        circle.rect[1] - aim_dist,
                        circle.rect[2] + aim_dist * 2,
                        circle.rect[3] + aim_dist * 2]
            if circle.color:
                aim_color = circle.color
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

            if angle1 and angle2 and circle.radius >= aim_fat:
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
                                         self.grid.color1,
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
            self.grid.game_display.blit(
                self.grid.mouse_img, self.set_img_pos(
                    current_tile,
                    self.grid.mouse_img))

    def draw_movement(self, circle):
        """ DEBUG: Shows the movement in cyan and the correct track in red """
        for move_step in circle.move_track:
            self.grid.pygame.draw.circle(self.grid.game_display,
                               self.grid.white,
                               move_step,
                               2,
                               1)

    def draw_msg(self):
        red_msg = [rep_msg.replace("_", ' ') for rep_msg in self.grid.reporting]
        red_msg.extend(['you dead'])
        red_msg.extend(self.grid.lose_msg)

        if self.grid.messages:
            for idx, msg in enumerate(self.grid.messages[-self.grid.max_msg:]):
                msg = msg.replace("SCREEN - ", "")
                font = getattr(self.grid.fonts, 'small')
                if "+" in msg or "-" in msg:
                    color = self.grid.c5c5c5
                elif any(rmsg in msg for rmsg in red_msg):
                    color = self.grid.ed6d31
                elif msg in self.grid.win_msg:
                    color = self.grid.fcc21c
                else:
                    color = self.grid.white

                # if idx == 0:
                #     color = self.grid.white
                # else:
                #     color = self.grid.color1

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

            if rradius < self.grid.tile_border:
                rradius = self.grid.tile_border
            self.grid.pygame.draw.circle(self.grid.game_display,
                                         self.grid.color1,
                                         rev_tile,
                                         rradius,
                                         self.grid.tile_border)
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

        all_circles =  self.grid.circles + self.grid.panel_circles.values()

        for circle in all_circles:
            if circle.available:

                # VIBE
                if circle.vibe_track['track']:
                    self.draw_vibe(circle)

                # CIRCLES
                self.draw_body(current_tile, circle)


                # SHOW MOVEMENT
                if self.grid.show_debug and len(circle.move_track) > 1:
                    self.draw_movement(circle)

                # TIMERS
                # self.draw_timers(circle)


        # MOUSE
        if self.grid.mouse_mode:
            self.draw_mouse_image(current_tile)

        # GRID
        if self.grid.show_debug:
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