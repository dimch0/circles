# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                   LOADER                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
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


class DataLoader(object):

    def __init__(self, grid=None):
        self.grid = grid
        self.csv_all = None
        self.csv_data = None
        self.data_file = None
        self.door_slots = self.grid.names_to_pos(["11_1", "16_6", "16_16", "11_21", "6_16", "6_6"])

    def set_data_file(self):
        """ Extends the current scenario data file with the all data file """
        lines_to_write = []

        # self.csv_all = csv_from_excel(self.grid.all)
        # self.csv_data = csv_from_excel(self.grid.data_file)

        self.csv_all = self.grid.all
        self.csv_data = self.grid.data_file

        with open(self.csv_all, 'rb') as all:
            data_all = csv.reader(all, delimiter=',')
            header_all = next(data_all)
            for line in data_all:
                if line and not line == header_all:
                    lines_to_write.append(line)

        with open(self.csv_data, 'ab') as data_file:
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
            self.grid.msg("ERROR - {0}, could not create item of klas: {1}".format(e, klas))

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
            self.grid.msg("ERROR - Could not set attribute: {0}".format(e))

        dummy.radius = self.grid.tile_radius
        dummy.default_radius = dummy.radius

        # DEBUG
        if self.grid.show_debug:
           self.grid.msg("DEBUG - Loaded {0}".format(dummy.name))

        return dummy

    def set_col_idx(self, header):
        """ Returns a dict with all columns as keys
        and their indexes as values """
        result = {}
        for idx, name in enumerate(header):
            result[name] = idx
        return result

    def load_data(self, item_name=None):
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
                            "type"        : str(row[col_idx["type"]]),
                            "has_opts"    : str(row[col_idx["has_opts"]]),
                            "category"    : str(row[col_idx["category"]]),
                            "available"   : bool(row[col_idx["available"]]),
                            "name"        : str(row[col_idx["name"]]),
                            "pos"         : self.grid.tile_dict[row[col_idx["pos"]]] if len(row[col_idx["pos"]]) > 0 else None,
                            "color"       : getattr(self.grid, row[col_idx["color"]]) if len(row[col_idx["color"]]) > 0 else None,
                            "img"         : getattr(self.grid.images, row[col_idx["img"]]) if len(row[col_idx["img"]]) > 0 else None,
                            "speed"       : int(float(row[col_idx["speed"]])) if len(row[col_idx["speed"]]) > 0 else None,
                            "range"       : int(float(row[col_idx["range"]])) if len(row[col_idx["range"]]) > 0 else None,
                            "time_color"  : getattr(self.grid, row[col_idx["time_color"]]) if len(row[col_idx["time_color"]]) > 0 else None,
                            "modable"     : bool(row[col_idx["modable"]]),
                            "collectible" : bool(row[col_idx["collectible"]]),
                            "consumable"  : bool(row[col_idx["consumable"]]),
                            "uses"        : int(float(row[col_idx["uses"]])) if len(row[col_idx["uses"]]) > 0 else 1,
                            "room"        : str(row[col_idx["room"]]),
                            "lifespan"    : float(row[col_idx["lifespan"]]) if len(row[col_idx["lifespan"]]) > 0 else None,
                            "vfreq"       : float(row[col_idx["vfreq"]]) if len(row[col_idx["vfreq"]]) > 0 else None,
                            "vspeed"      : int(float(row[col_idx["vspeed"]])) if len(row[col_idx["vspeed"]]) > 0 else 1,
                            "layer"       : int(float(row[col_idx["layer"]])) if len(row[col_idx["layer"]]) > 0 else 1,
                            "effects"     : str(row[col_idx["effects"]])
                        }

                        # CREATE ITEM
                        if item_name:
                            if item_name in attributes_dict["name"]:
                                item = self.create_new_item(klas, attributes_dict)
                            else:
                                continue
                        else:
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
                # item.default_options[opt.name] = opt

    def set_opts(self, item):
        if item.has_opts:
            for opt, klas in self.load_data():
                self.find_opts(opt, item)
                if opt.has_opts:
                    for sub_opt, klas in self.load_data():
                        self.find_opts(sub_opt, opt)
            if self.grid.show_debug:
                self.grid.msg("DEBUG - {0} options are: {1}".format(item.name, item.options))


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


        if hasattr(item, "vfreq"):
            vibefr = cir_item_timer.TimerItem()
            vibefr.duration = item.vfreq
            item.vfreq = vibefr


    def load_item(self, item_name):
        new_item = None
        for item, klas in self.load_data(item_name):
            if item.name == item_name:
                new_item = item
                self.set_timers(new_item)
                break
        return new_item

    def set_door(self, item):
        door = cir_item.Item()
        door.type = item.type
        door.name = "Enter_" + item.room
        door.room = item.name.replace("Enter_", "")
        door.pos = cir_utils.get_mirror_point(item.pos, self.grid.center_tile)
        door.color = item.color
        if "door_enter" in item.type:
            door.img = self.grid.images.neon_exit
        else:
            door.img = item.img
        door.default_img = item.default_img
        door.default_color = item.color
        door.radius = item.radius
        door.default_radius = item.radius
        door.available = True

        self.set_room(door)
        self.set_timers(door)


    def set_buttons(self):
        """ Assign all items to the grid object """

        for name in ["play", "quit"]:
            butt = cir_item_button.ButtonItem()
            butt.name = name
            # butt.color = self.grid.room_color
            butt.font = getattr(self.grid.fonts, 'small')
            butt.text_color = self.grid.white
            if name == "play":
                butt.pos = self.grid.tile_dict['11_9']
            elif name == "quit":
                butt.pos = self.grid.tile_dict['11_13']

            self.grid.buttons.append(butt)



    def set_room(self, item):
        if item.room not in [None, ""]:
            if item.room not in self.grid.rooms.keys():
                self.grid.rooms[item.room] = {
                        "items"          : [],
                        "revealed_tiles" : {}
                                             }
            self.grid.rooms[item.room]["items"].append(item)

    def set_door_plugs(self):
        for room, value in self.grid.rooms.items():
            room_door_pos = []
            for door_item in value["items"]:
                if "door" in  door_item.type:
                    if not door_item.pos in room_door_pos:
                        room_door_pos.append(door_item.pos)

            plugs_pos = list(set(self.door_slots) - set(room_door_pos))

            for plug_pos in plugs_pos:
                plug = self.load_item("plug")
                plug.name = plug.name + str(time.time())
                time.sleep(0.001)
                plug.color = self.grid.fog_color
                plug.pos = plug_pos
                plug.available = True
                value["items"].append(plug)


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
        my_body_inventory = None

        self.grid.msg("INFO - Loading {0}".format(self.grid.scenario))
        for item, klas in self.load_data():

            if item.type == "editor" and self.grid.show_editor:
                item.room = "ALL"
            elif "door" in item.type:
                self.set_door(item)
            elif item.type == "my_body":
                my_body = item
                my_body.gen_birth_track()
            elif item.type == "inventory":
                my_body_inventory = item

            self.set_room(item)
            self.set_timers(item)
            self.set_opts(item)



        if not my_body in self.grid.items:
            self.grid.items.append(my_body)


        if self.grid.scenario in ["scenario_1"]:

            self.grid.fog_color = self.grid.grey01
            self.grid.room_color = self.grid.grey03
            self.set_door_plugs()


        # elif self.grid.scenario in ["scenario_2"]:
        #     self.grid.fog_color = self.grid.pink
        #     self.grid.room_color = self.grid.black
        #     self.grid.game_menu = False
        self.set_buttons()
        self.grid.load_current_room()


        my_body.inventory = my_body_inventory
        return my_body