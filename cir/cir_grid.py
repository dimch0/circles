# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                                                                                     #
#                                                     GRID                                                            #
#                                                                                                                     #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import os
import time
import json
from math import sqrt

from cir_utils import in_circle, inside_polygon, bcolors, get_short_name, intersecting

CONFIG_JSON_FILE = "config.json"


class Grid(object):
    """ master class for the grid """

    def __init__(self, pygame=None, scenario=None):
        # -------------------------------------------------- #
        #                      HELPERS                       #
        # -------------------------------------------------- #
        self.pygame = pygame
        self.scenario = scenario
        self.images = None
        self.fonts = None
        self.drawer = None
        self.loader = None
        self.updater = None
        self.event_effects = None
        # -------------------------------------------------- #
        #                      SETTINGS                      #
        # -------------------------------------------------- #
        self.cathetus = 0
        self.display_width = 0
        self.display_height = 0
        self.game_display = None
        self.fog_color = None
        self.color1 = None
        self.door_slots = []
        self.set_config()
        self.data_file = os.path.join(
            self.data_dir,
            # self.scenario,
            "scenario_01",
            "data.csv")
        self.game_menu = True
        self.game_over = False
        self.start_time = None
        self.shift = False
        self.seconds_in_game = 0
        self.seconds_in_pause = 0
        self.clock = pygame.time.Clock()
        self.messages = []
        # -------------------------------------------------- #
        #                        TILES                       #
        # -------------------------------------------------- #
        # TODO: Remove tile_dict and change tiles to a dict
        self.tiles = []
        self.tile_dict = {}
        self.set_display()
        self.center_tile = None
        self.previous_tile = None
        self.find_center_tile()
        self.set_playing_tiles()
        self.occupado_tiles = {}
        self.revealed_tiles = {}
        self.total_revealed = 0
        self.draw_map = False
        self.map_dots = {}
        self.tile_border = self.tile_radius / 15
        # -------------------------------------------------- #
        #                        ROOMS                       #
        # -------------------------------------------------- #
        self.rooms = {}
        self.current_room = "11_11"
        self.previous_room = None
        self.needs_to_change_room = False
        # -------------------------------------------------- #
        #                        ITEMS                       #
        # -------------------------------------------------- #
        self.items = []
        self.overlap = []
        self.buttons = []
        self.editor_buttons = []
        self.panel_items = {}
        # -------------------------------------------------- #
        #                        MOUSE                       #
        # -------------------------------------------------- #
        self.mouse_mode = None
        self.mouse_img = None
        self.mode_img = None
        # -------------------------------------------------- #
        #                        KEYS                        #
        # -------------------------------------------------- #
        self.arrows = [self.pygame.K_w,
                       self.pygame.K_e,
                       self.pygame.K_d,
                       self.pygame.K_s,
                       self.pygame.K_a,
                       self.pygame.K_q]

    # --------------------------------------------------------------- #
    #                            SETTINGS                             #
    # --------------------------------------------------------------- #
    def set_game_display(self):
        self.game_display = self.pygame.display.set_mode((self.display_width, self.display_height))


    def read_config(self, conf_file, reccur=True):
        if os.path.exists(conf_file):
            with open(conf_file) as jsonfile:
                conf = json.load(jsonfile)
                if reccur:
                    for section in conf.keys():
                        for metric, value in conf[section].items():
                            setattr(self, metric, value)
                else:
                    for metric, value in conf.items():
                        setattr(self, metric, value)

        else:
            self.msg('ERROR - No such file: {0}'.format(conf_file))

    def set_config(self):
        """
        Setting attributes from the config.json file
        and calculating the display metrics
        """
        try:
            self.read_config(CONFIG_JSON_FILE)
            conf_scenario = os.path.join(self.data_dir, self.scenario, 'config.json')
            self.read_config(conf_scenario, reccur=False)
        except Exception as e:
            self.msg("ERROR - Could not set config: {0}".format(e))

    def set_display(self):
        self.cathetus = int(sqrt(((2 * self.tile_radius) ** 2) - (self.tile_radius ** 2)))
        self.display_width = (self.cathetus * self.cols) + (self.tile_radius * 2)
        self.display_height = self.rows * self.tile_radius
        self.set_game_display()
        self.pygame.display.set_caption(self.caption)
        self.gen_tiles()

    # --------------------------------------------------------------- #
    #                             TILES                               #
    # --------------------------------------------------------------- #
    def gen_tiles(self):
        """ Generating the grid tiles """
        self.tiles = []
        for x in range(0, self.cols + 1):
            for y in range(1, self.rows):
                if x % 2 == y % 2:
                    centre_x = self.tile_radius + (x * self.cathetus)
                    centre_y = y * self.tile_radius
                    centre = (centre_x, centre_y)
                    if not centre in self.tiles:
                        self.tiles.append(centre)
                        self.tile_dict[str(x) + '_' + str(y)] = centre
        self.tile_dict['center'] = self.find_center_tile()


    def find_center_tile(self):
        """ :return: the center tile (x, y) of the grid """

        mid_x = int(self.display_width / 2)
        mid_y = int(self.display_height / 2)
        for tile in self.tiles:
            if in_circle(tile, self.tile_radius, (mid_x, mid_y)):
                self.center_tile = tile
                break
        return self.center_tile

    def mouse_in_tile(self, MOUSE_POS):
        """
        :param MOUSE_POS: position of the mouse
        :return: returns the current tile, the mouse is in
         or None if there is no such
        """
        current_tile = None
        for tile in self.tiles:
            if in_circle(tile, self.tile_radius, MOUSE_POS):
                current_tile = tile

        if current_tile:
            self.previous_tile = current_tile
        elif not current_tile and self.previous_tile:
            current_tile = self.previous_tile

        return current_tile

    def names_to_pos(self, names):
        """ Returns a list of pos tuples """

        result = None

        if isinstance(names, list):
            result = []
            for name in names:
                for tile_name, tile_pos in self.tile_dict.items():
                    if tile_name == name:
                        result.append(tile_pos)
        else:
            for tile_name, tile_pos in self.tile_dict.items():
                if tile_name == names:
                    result = tile_pos

        return result

    def pos_to_name(self, pos):
        """ Returns name from pos """
        for tile_name, tile_pos in self.tile_dict.items():
            if tile_pos == pos:
                return tile_name

    def set_playing_tiles(self):
        """ Defining the playing tiles """
        if self.playing_tiles:
            self.playing_tiles = self.names_to_pos(self.playing_tiles)
            inside_tiles = []
            for tile in self.tiles:
                if inside_polygon(self.playing_tiles, tile):
                    if not tile in self.playing_tiles:
                        if not tile in inside_tiles:
                            inside_tiles.append(tile)
            self.playing_tiles.extend(inside_tiles)

        if self.door_slots:
            self.door_slots = self.names_to_pos(self.door_slots)

    def adj_tiles(self, center, empty=False, playing=False):
        """
        :param grid: the center tile
        :return: a list of 6 adjacent to the center tiles
        """
        self_x = center[0]
        self_y = center[1]
        adj_tiles = [
            (self_x, self_y - 2 * self.tile_radius),
            (self_x + self.cathetus, self_y - self.tile_radius),
            (self_x + self.cathetus, self_y + self.tile_radius),
            (self_x, self_y + 2 * self.tile_radius),
            (self_x - self.cathetus, self_y + self.tile_radius),
            (self_x - self.cathetus, self_y - self.tile_radius)]

        if empty:
            # empty_tiles = [tile for tile in adj_tiles if tile in self.revealed_tiles.keys()]
            for adj_tile in adj_tiles:
                if adj_tile in self.revealed_tiles.keys():
                    return adj_tile
        elif playing:
            for adj_tile in adj_tiles:
                if adj_tile in self.playing_tiles:
                    return adj_tile
        else:
            return adj_tiles


    def clean_placeholders(self, item):
        """ Cleans the placeholders (eg for mitosis) """
        if "placeholder" in item.name and 'option' not in item.type:
            for other_item in self.items:
                if other_item.pos == item.pos:
                    try:
                        item.available = False
                        self.items.remove(item)
                    except Exception as e:
                        self.msg("ERROR - ERROR Could not remove placeholder: {0}".format(e))

    def set_occupado(self):
        nonoccupado = ["signal",
                       "trigger",
                       "option"]
        tiles_to_check = set(self.playing_tiles + self.door_slots)
        for item in self.items:
            if not any(nonocc in item.type for nonocc in nonoccupado):
                for tile in tiles_to_check:
                    circle_1 = (tile, self.tile_radius)
                    circle_2 = (item.pos, self.tile_radius)
                    if intersecting(circle_1, circle_2):
                        self.occupado_tiles[item.name] = tile


    # --------------------------------------------------------------- #
    #                            MAP                                  #
    # --------------------------------------------------------------- #

    def get_map_dot(self, pos, room_pos, dot_col, dot_rad):
        """
        Gen map dot pos and return a dict
        :param pos:
        :param room_pos:
        :return: dict:
        'dot_pos' : {'pos': dot_pos,
                     'color': dot_col,
                     'radius': dot_rad}
        """
        result = {}
        map_scale = 10

        dix = (self.center_tile[0] - pos[0]) / map_scale
        diy = (self.center_tile[1] - pos[1]) / map_scale
        dot_pos = (room_pos[0] - dix, room_pos[1] - diy)

        result[dot_pos] = {'pos': dot_pos,
                           'color': dot_col,
                           'radius': dot_rad / map_scale}
        return result


    def gen_map_dots(self):
        map_dots = {}

        reddots = ['door_enter']
        whitedots = []
        gelbdots = ['my_body']
        ignoredots = ['editor', 'my_body', 'option', 'signal', 'inventory', 'slab']
        ignoredots += whitedots
        ignoredots += reddots

        for room_name, room  in self.rooms.items():
            if room_name not in ['map', 'ALL']:
                if self.names_to_pos([room_name]):
                    room_pos = self.names_to_pos([room_name])[0]

                    for tile in room['revealed_tiles']:
                        map_dots.update(self.get_map_dot(tile, room_pos, self.color1, self.tile_radius))

                    for item in room['items']:
                        if item.color and item.available:
                            if not any (ign in item.type for ign in ignoredots):
                                map_dots.update(self.get_map_dot(item.pos, room_pos, item.color, item.radius))

                            if any(reddot in item.type for reddot in reddots):
                                map_dots.update(self.get_map_dot(item.pos, room_pos, self.red01, item.radius))

                            if any(whitedot in item.type for whitedot in whitedots) and room_name == self.previous_room:
                                map_dots.update(self.get_map_dot(item.pos, room_pos, self.white, item.radius))

                            if any(gelbdot in item.type for gelbdot in gelbdots) and room_name == self.previous_room:
                                map_dots.update(self.get_map_dot(item.pos, room_pos, self.gelb05, item.radius))

        self.map_dots = map_dots

    # --------------------------------------------------------------- #
    #                             MOUSE                               #
    # --------------------------------------------------------------- #
    def clean_mouse(self):
        self.mouse_mode = None
        self.mouse_img = None

    def set_mouse_mode(self, option):

        new_mode = get_short_name(option.name)
        if self.mouse_mode == option.name:
            self.clean_mouse()
        else:
            self.mouse_mode = new_mode
            if option.img:
                self.mouse_img = option.img
            else:
                self.mouse_img = None



    # --------------------------------------------------------------- #
    #                             ROOMS                               #
    # --------------------------------------------------------------- #
    def save_current_room(self):
        """ Saves the current room to self.rooms """
        self.rooms[self.current_room] = {
            "items": self.items,
            "revealed_tiles": self.revealed_tiles
        }

    def load_current_room(self):
        """ loads the current room from self.rooms
        or an empty room if the number is not in self.rooms """
        self.msg("INFO - Loading room: {0}".format(self.current_room))
        self.occupado_tiles = {}

        # NEW ROOM
        if not self.current_room in self.rooms.keys():
            self.rooms[self.current_room] = {
            "items"          : [],
            "revealed_tiles": {},
            }
        self.items = self.rooms[self.current_room]["items"]
        self.items = list(set(self.items))
        self.revealed_tiles = self.rooms[self.current_room]["revealed_tiles"]

    def change_room(self, room):
        """ Saves the current room and loads a new room """
        self.save_current_room()
        self.current_room = str(room)
        self.load_current_room()
        self.needs_to_change_room = False

    # --------------------------------------------------------------- #
    #                            SECONDS                              #
    # --------------------------------------------------------------- #
    def seconds_in_game_tick(self):
        """ Counts the seconds in the game """

        if time.time() > self.start_time + self.seconds_in_game + self.seconds_in_pause:
            if not self.game_menu and not self.current_room in ["map"]:
                self.seconds_in_game += 1
                if self.show_seconds:
                    self.msg("INFO - Game second: {0}".format(self.seconds_in_game))
            else:
                self.seconds_in_pause += 1
                if self.show_seconds:
                    self.msg("INFO - Pause second: {0}".format(self.seconds_in_pause))

    # --------------------------------------------------------------- #
    #                            ITEMS                                #
    # --------------------------------------------------------------- #
    def rename_button(self, old_name, new_name):
        for button in self.buttons:
            if button.name == old_name:
                button.name = new_name

    def sort_items_by_layer(self):
        self.items.sort(key=lambda x: x.layer, reverse=False)

    # --------------------------------------------------------------- #
    #                            GAME EXIT                            #
    # --------------------------------------------------------------- #
    # def clean_tmp_dir(self):
    #     for file in os.listdir(self.tmp_dir):
    #         file = os.path.join(self.tmp_dir, file)
    #         os.remove(file)
    #         self.msg("INFO - Removed: {0}".format(file))

    def game_exit(self):
        # self.clean_tmp_dir()
        self.pygame.quit()
        self.msg("SCREEN - game finish")
        quit()

    # --------------------------------------------------------------- #
    #                            LOG MSG                              #
    # --------------------------------------------------------------- #
    def log_msg(self, msg):
        """ Log a message in a temp log file """
        if not self.messages or (self.messages and not msg == self.messages[-1]):
            self.messages.append(msg)
            # self.messages.insert(0, msg) # append the item at the beginning of the list

        if len(self.messages) > 36:
            self.messages.pop(0)

    def msg(self, msg):
        """ Display messages in terminal """
        will_show_msg = True
        msg_color = bcolors.INFO
        msg = msg.replace('my_body', 'you')

        if not self.show_debug and "DEBUG - " in msg:
            will_show_msg = False
            msg_color = bcolors.DEBUG
        if not self.show_verbose and "INFO - " in msg:
            will_show_msg = False
            msg_color = bcolors.INFO
        if "ERROR - " in msg:
            msg_color = bcolors.ERROR
        if "SCREEN - " in msg:
            msg_color = bcolors.BOLD
            self.log_msg(msg)

        if will_show_msg:
            print(msg_color + msg + bcolors.ENDC)
