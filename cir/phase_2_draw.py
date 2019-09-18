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
        self.time_vs_max = ()
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
                # TODO:
                circle.effect_track = []

            self.draw_img(circle)
            self.draw_hover(current_tile, circle)

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
        self.grid.pygame.draw.circle(self.grid.game_display,
                                     self.grid.white,
                                     circle.target_tile,
                                     2,
                                     1)


    def draw_time(self):
        if self.time_vs_max:
            msg = "%s/%s" % (self.time_vs_max[0], self.time_vs_max[1])
            font = getattr(self.grid.fonts, 'small')
            color = self.grid.white
            txt = font.render(msg, True, color)
            txt_rect = self.grid.pygame.Rect(20, 20, 20, 20)
            txt_rect.center = (self.grid.tile_dict["21_1"][0], self.grid.tile_dict["21_1"][1])
            self.grid.game_display.blit(txt, txt_rect)

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

        # MOUSE
        if self.grid.mouse_mode:
            self.draw_mouse_image(current_tile)

        # GRID
        if self.grid.show_debug:
            self.draw_grid()

        # MSG
        self.draw_msg()
        self.draw_time()

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