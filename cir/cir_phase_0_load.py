#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                                    Loader Class                                     #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
import csv
import cir_item
import cir_item_body
import cir_item_timer
import cir_item_button
import cir_utils


class DataLoader(object):

    def __init__(self, grid=None):
        self.grid = grid


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
            print("ERROR: {0}, could not create item of klas: {1}".format(e, klas))

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
            print("ERROR: Could not set attribute: {0}".format(e))

        dummy.radius = self.grid.tile_radius
        dummy.default_radius = dummy.radius

        # DEBUG
        if self.grid.show_debug:
            print("DEBUG: Loaded {0}".format(dummy.name))
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
        :param images:  images instance
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
                print("DEBUG: {0} options are: {1}".format(item.name, item.options))
                # print(item.name, [opt.name + " - " + str([sopt.name for sopt in opt.options]) for opt in item.options])


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
        door.type = "other side"
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


    def load_items(self):
        """
        Loading all modes, buttons, timers, my_body
        :return: my_body
        """
        print("INFO: Loading items: {0}".format(self.grid.scenario))
        my_body = None
        for item, klas in self.load_data():
            # EDITOR
            if item.type == "editor" and self.grid.show_editor:
                item.room = "ALL"
            # SET ROOM
            self.set_room(item)
            # SET_TIMERS
            self.set_timers(item)
            # SET OPTS
            self.set_opts(item)
            # SET DOOR
            if item.type == "door":
                self.set_door(item)
            # MY BODY
            elif item.type == "my_body":
                my_body = item
                my_body.gen_birth_track()

        self.set_buttons()
        self.grid.load_current_room()

        return my_body