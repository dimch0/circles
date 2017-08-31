#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                                    Loader Class                                     #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
import csv
import time

import cir_item
import cir_item_body
import cir_item_timer
import cir_item_button
import cir_utils

from cir_cosmetic import Images, Fonts, Colors
from cir_phase_1_events import GameEvents
from cir_phase_2_draw import GameDrawer
from cir_phase_3_update import VarUpdater
from cir.cir_logger import CirLogger


class DataLoader(object):

    def __init__(self, grid=None):
        self.grid = grid
        self.logger = None
        self.set_logger()


    def set_logger(self):
        self.grid.logger = CirLogger()
        self.logger = self.grid.logger

    def set_data_file(self):
        """ Extends the current scenario data file with the all data file """
        lines_to_write = []
        with open(self.grid.all, 'rb') as all:
            data_all = csv.reader(all, delimiter=',')
            header_all = next(data_all)
            for line in data_all:
                if line and not line == header_all:
                    lines_to_write.append(line)

        with open(self.grid.data_file, 'ab') as data_file:
            writer = csv.writer(data_file)
            for line in lines_to_write:
                writer.writerow(line)

    def create_new_item(self, klas, attributes_dict):
        """
        This function creates an item of a class by the given klas.
        Attributes are set by a given dict (attributes_dict)
        :param klas: klas specified
        :param attributes_dict: generated dict
        :return: a new instance of an item object
        """
        dummy = None
        try:
            if klas == "body":
                dummy = cir_item_body.BodyItem()
            elif klas == "timer":
                dummy = cir_item_timer.TimerItem()
                dummy.timer_tile_radius = self.grid.tile_radius
            elif klas in "item":
                dummy = cir_item.Item()
        except Exception as e:
            self.logger.log(self.logger.ERROR, "{0}, could not create item of klas: {1}".format(e, klas))

        try:
            for attribute, value in attributes_dict.items():
                if dummy:
                    if hasattr(dummy, attribute):
                        setattr(dummy, attribute, value)
                    if attribute == "img":
                        if hasattr(dummy, "default_img"):
                            setattr(dummy, "default_img", value)
                    if attribute == "color":
                        if hasattr(dummy, "default_color"):
                            setattr(dummy, "default_color", value)

        except Exception as e:
            self.logger.log(self.logger.ERROR, "Could not set attribute: {0}".format(e))

        dummy.radius = self.grid.tile_radius
        dummy.default_radius = dummy.radius

        # DEBUG
        if self.grid.show_debug:
           self.logger.log(self.logger.DEBUG, "Loaded {0}".format(dummy.name))

        return dummy

    def set_col_idx(self, header):
        """ Returns a dict with all columns as keys
        and their indexes as values """
        result = {}
        for idx, name in enumerate(header):
            result[name] = idx
        return result

    def load_data(self):
        """
        This function loads all items and menu options from external data file.
        :param images: images instance
        :return: item object, type and category
        """
        with open(self.grid.data_file, 'rb') as csvfile:
            data = csv.reader(csvfile, delimiter=',')
            header = next(data)
            col_idx = self.set_col_idx(header)
            for row in data:
                if not row == header:
                    scenario_col = row[col_idx["scenario"]]
                    if str(self.grid.scenario) in scenario_col or "ALL" in scenario_col:
                        klas = row[col_idx["klas"]]
                        # --------------------------------------------------------------- #
                        #                        ATTRIBUTES DICT                          #
                        # --------------------------------------------------------------- #
                        attributes_dict = {
                            "type"        : row[col_idx["type"]],
                            "has_opts"    : row[col_idx["has_opts"]],
                            "category"    : row[col_idx["category"]],
                            "available"   : bool(row[col_idx["available"]]),
                            "name"        : row[col_idx["name"]],
                            "pos"         : self.grid.tile_dict[row[col_idx["pos"]]] if len(row[col_idx["pos"]]) > 0 else None,
                            "color"       : getattr(self.grid, row[col_idx["color"]]) if len(row[col_idx["color"]]) > 0 else None,
                            "img"         : getattr(self.grid.images, row[col_idx["img"]]) if len(row[col_idx["img"]]) > 0 else None,
                            "speed"       : int(row[col_idx["speed"]]) if len(row[col_idx["speed"]]) > 0 else None,
                            "range"       : int(row[col_idx["range"]]) if len(row[col_idx["range"]]) > 0 else None,
                            "time_color"  : getattr(self.grid, row[col_idx["time_color"]]) if len(row[col_idx["time_color"]]) > 0 else None,
                            "modable"     : bool(row[col_idx["modable"]]),
                            "collectible" : bool(row[col_idx["collectible"]]),
                            "consumable"  : bool(row[col_idx["consumable"]]),
                            "uses"        : int(row[col_idx["uses"]]) if len(row[col_idx["uses"]]) > 0 else None,
                            "room"        : row[col_idx["room"]],
                            "lifespan"    : float(row[col_idx["lifespan"]]) if len(row[col_idx["lifespan"]]) > 0 else None,
                            "vibe_freq"   : float(row[col_idx["vibe_freq"]]) if len(row[col_idx["vibe_freq"]]) > 0 else None
                        }

                        # CREATE ITEM
                        item = self.create_new_item(klas, attributes_dict)
                        yield item, klas

    def find_opts(self, opt, item):
        if opt.type == "option":
            if opt.category and opt.category in item.name:
                if not opt.color:
                    opt.color = item.color
                opt.default_color = item.color
                # item.options.append(opt)
                item.options[opt.name] = opt
                item.default_options[opt.name] = opt

    def set_opts(self, item):
        if item.has_opts:
            for opt, klas in self.load_data():
                self.find_opts(opt, item)
                if opt.has_opts:
                    for sub_opt, klas in self.load_data():
                        self.find_opts(sub_opt, opt)
            if self.grid.show_debug:
                self.logger.log(self.logger.DEBUG, "{0} options are: {1}".format(item.name, item.options))


    def set_timers(self, item):
        """ Set timers """
        if item.lifespan:
            lifespan = cir_item_timer.TimerItem()
            lifespan.radius = self.grid.tile_radius
            lifespan.default_radius = self.grid.tile_radius
            lifespan.duration = item.lifespan
            lifespan.limit = lifespan.duration
            lifespan.color = item.time_color
            item.lifespan = lifespan

        if item.birth_time:
            birth = cir_item_timer.TimerItem()
            birth.duration = item.birth_time
            item.birth_time = birth

        if hasattr(item, "vibe_freq"):
            vibefr = cir_item_timer.TimerItem()
            vibefr.duration = item.vibe_freq
            item.vibe_freq = vibefr

    def set_door(self, item):
        door = cir_item.Item()
        door.type = "door"
        door.name = "Enter_" + item.room
        door.room = item.name.replace("Enter_", "")
        door.pos = cir_utils.get_mirror_point(item.pos, self.grid.center_tile)
        door.color = item.color
        door.img = item.img
        door.default_img = item.default_img
        # door.options = item.options
        # door.default_options = door.default_options
        door.default_color = door.default_color
        door.radius = item.radius
        door.default_radius = item.radius
        door.available = False

        self.set_room(door)
        self.set_timers(door)


    def set_buttons(self):
        """ Assign all items to the grid object """

        for name in ["play", "quit"]:
            butt = cir_item_button.ButtonItem()
            butt.name = name
            butt.color = self.grid.grey
            butt.font = getattr(self.grid.fonts, 'small')
            butt.text_color = self.grid.white
            if name == "play":
                butt.pos = self.grid.tile_dict['12_10']
            elif name == "quit":
                butt.pos = self.grid.tile_dict['12_14']

            self.grid.buttons.append(butt)


    def set_room(self, item):
        if item.room not in [None, ""]:
            if item.room not in self.grid.rooms.keys():
                self.grid.rooms[item.room] = {
                    "items"          : [],
                    "revealed_radius": []}
            self.grid.rooms[item.room]["items"].append(item)



    def load_item(self, item_name):
        new_item = None
        for item, klas in self.load_data():
            if item.name == item_name:
                new_item = item
                self.set_timers(new_item)
                break
        return new_item


    def load_game(self):
        """
        Main loading execution of all items, cosmetics and preconditions
        :return: my_body
        """

        Colors.set_colors(self.grid)
        self.grid.images        = Images(self.grid)
        self.grid.fonts         = Fonts(self.grid)
        self.set_data_file()
        self.grid.event_effects = GameEvents(self.grid)
        self.grid.drawer        = GameDrawer(self.grid)
        self.grid.updater       = VarUpdater(self.grid)
        self.grid.start_time    = time.time()

        my_body = None

        self.logger.log(self.logger.INFO, "Loading {0}".format(self.grid.scenario))
        for item, klas in self.load_data():

            if item.type == "editor" and self.grid.show_editor:
                item.room = "ALL"
            elif item.type == "door":
                self.set_door(item)
            elif item.type == "my_body":
                my_body = item
                my_body.gen_birth_track()

            self.set_room(item)
            self.set_timers(item)
            self.set_opts(item)

        self.set_buttons()
        self.grid.load_current_room()

        if not my_body in self.grid.items:
            self.grid.items.append(my_body)


        if self.grid.scenario == "scenario_1":
            self.grid.fog_color = self.grid.dark_grey
            self.grid.room_color = self.grid.grey

        elif self.grid.scenario == "scenario_2":
            self.grid.fog_color = self.grid.dark_grey
            self.grid.room_color = self.grid.black
            self.grid.game_menu = False

        # self.grid.clean_tmp_maps()

        return my_body