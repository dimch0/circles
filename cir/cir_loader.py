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
import cir_item_mobile


class DataLoader(object):

    def __init__(self, grid=None):
        self.grid = grid


    def create_new_item(self, type, attributes):
        """
        This function creates an item of a class by the given type.
        Attributes are set by a given dict (attributes)
        :param type: type specified
        :param attributes: generated dict
        :return: a new instance of an item object
        """
        dummy = None
        try:
            if type in ["body", "trigger"]:
                dummy = cir_item_body.BodyItem()
            elif type == "timer":
                dummy = cir_item_timer.TimerItem()
                dummy.timer_tile_radius = self.grid.tile_radius
            elif type in ["mobile", "signal"]:
                dummy = cir_item_mobile.MobileItem()
            elif type in ["mode_option", "simple"]:
                dummy = cir_item.Item()
        except Exception as e:
            print("Error {0, could not create item of type: {1}".format(e, type))

        try:
            for attribute, value in attributes.items():
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
            print "Error, could not set attribute: {0}".format(e)

        dummy.radius = self.grid.tile_radius
        dummy.default_radius = dummy.radius

        # DEBUG PRINT
        if self.grid.show_debug:
            print"Loaded {0}".format(dummy.name)
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
                        category = row[col_idx["category"]]
                        type = row[col_idx["type"]]
                        # --------------------------------------------------------------- #
                        #                        ATTRIBUTES DICT                          #
                        # --------------------------------------------------------------- #
                        attributes = {
                            "type"        : row[col_idx["type"]],
                            "available"   : bool(row[col_idx["available"]]) if len(row[col_idx["available"]]) > 0 else None,
                            "name"        : row[col_idx["name"]] if len(row[col_idx["name"]]) > 0 else None,
                            "pos"         : self.grid.tile_dict[row[col_idx["pos"]]] if len(row[col_idx["pos"]]) > 0 else None,
                            "color"       : getattr(self.grid, row[col_idx["color"]]) if len(row[col_idx["color"]]) > 0 else None,
                            "img"         : getattr(self.grid.images, row[col_idx["img"]]) if len(row[col_idx["img"]]) > 0 else None,
                            "speed"       : int(row[col_idx["speed"]]) if len(row[col_idx["speed"]]) > 0 else None,
                            "range"       : int(row[col_idx["range"]]) if len(row[col_idx["range"]]) > 0 else None,
                            "time_color"  : getattr(self.grid, row[col_idx["time_color"]]) if len(row[col_idx["time_color"]]) > 0 else None,
                            "modable"     : row[col_idx["modable"]] if len(row[col_idx["modable"]]) > 0 else None,
                            "collectible" : row[col_idx["collectible"]] if len(row[col_idx["collectible"]]) > 0 else None,
                            "uses"        : int(row[col_idx["uses"]]) if len(row[col_idx["uses"]]) > 0 else None,
                            "room"        : row[col_idx["room"]] if len(row[col_idx["room"]]) > 0 else None,
                            "lifespan"    : float(row[col_idx["lifespan"]]) if len(row[col_idx["lifespan"]]) > 0 else None,
                            "vibe_freq"   : float(row[col_idx["vibe_freq"]]) if len(row[col_idx["vibe_freq"]]) > 0 else None
                        }

                        # Create an items
                        item = self.create_new_item(type, attributes)
                        yield item, type, category


    def add_optoin_to_mode(self, category, option):
        """ Append the mode option to the MODE_VS_OPTIONS DICT """
        if category not in self.grid.mode_vs_options.keys():
            self.grid.mode_vs_options[category] = []
        self.grid.mode_vs_options[category].append(option)


    def set_mode_options(self):
        """ Assign all options from grid.mode_vs_options to grid.items """
        for name, item in self.grid.everything.items():
            for mode_name, mode_options in self.grid.mode_vs_options.items():
                if mode_name in item.name:
                    item.default_options = mode_options
                    item.options = item.default_options

    def set_timer(self, item):
        """ Assign all options from self.grid.mode_vs_options to grid.items """
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
            self.grid.everything[butt.name] = butt


    def set_rooms(self, item):
        if item.room not in [None, ""]:
            if item.room not in self.grid.rooms.keys():
                self.grid.rooms[item.room] = {
                    "items"          : [],
                    "revealed_radius": []
                }
            self.grid.rooms[item.room]["items"].append(item)


    def load_item(self, item_name):
        new_item = None
        for item, type, category in self.load_data():
            if item.name == item_name:
                new_item = item
                self.set_timer(new_item)
                break
        return new_item


    def load_editor(self):
        print("Loading editor mode ...")
        editor_items = []
        for item, type, category in self.load_data():
            if "EDITOR" in item.name:
                editor_items.append(item)
        return editor_items


    def load_items(self):
        """
        Loading all modes, buttons, timers, my_body
        :return: my_body
        """
        print("Loading from {} ...".format(self.grid.scenario))
        for item, type, category in self.load_data():
            # Everything
            self.grid.everything[item.name] = item
            self.set_rooms(item)
            self.set_timer(item)
            # Mode options
            if type == "mode_option":
                self.add_optoin_to_mode(category, item)

        self.set_buttons()
        self.set_mode_options()
        my_body = self.grid.everything["my_body"]
        my_body.gen_birth_track()
        self.grid.rooms[self.grid.current_room]["revealed_radius"].append(((my_body.pos), self.grid.tile_radius))
        self.grid.load_current_room()

        return my_body