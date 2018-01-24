# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                   LOADER                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import csv
import time

import cir_utils as cu

from cir_item import Item
from cir_item_body import BodyItem
from cir_item_body_scout import Scout
from cir_item_body_spawn import Spawn
from cir_item_timer import TimerItem

from cir_cosmetic import Images, Fonts, Colors
from cir_phase_1_events import GameEvents
from cir_phase_2_draw import GameDrawer
from cir_phase_3_update import VarUpdater


class DataLoader(object):

    def __init__(self, grid=None):
        self.grid = grid
        self.csv_data = self.grid.data_file
        self.data_file = None
        self.my_body = None

    def set_data_file(self):
        """ Extends the current scenario data file with the all data file """
        lines_to_write = []
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
                dummy = BodyItem()
            elif klas == "timer":
                dummy = TimerItem()
                dummy.timer_tile_radius = self.grid.tile_radius
            elif klas == "item":
                dummy = Item()
            elif klas == "scout":
                dummy = Scout()
            elif klas == "spawn":
                dummy = Spawn()
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

                    elif attribute == "color":
                        if hasattr(dummy, "default_color"):
                            setattr(dummy, "default_color", value)

                    elif attribute == "effects":
                        if "#hunger" in value:
                            dummy.hungry = True

        except Exception as e:
            self.grid.msg("ERROR - Could not set attribute: {0}".format(e))

        try:
            dummy.radius = self.grid.tile_radius
            dummy.default_radius = dummy.radius
        except Exception as e:
            self.grid.msg("ERROR - Could not set radius: %s" % e)
            self.grid.msg("ERROR - dummy: %s" % dummy)
            self.grid.msg("ERROR - klas: %s" % klas)
            self.grid.msg("ERROR - attributes: %s" % attributes_dict)

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
                    if len([field for field in row if field not in [None, '']]) > 1:
                        klas = row[col_idx["klas"]]
                        # --------------------------------------------------------------- #
                        #                        ATTRIBUTES DICT                          #
                        # --------------------------------------------------------------- #
                        try:
                            attributes_dict = {
                                "type"        : str(row[col_idx["type"]]),
                                "options"    : str(row[col_idx["options"]]),
                                "name"        : str(row[col_idx["name"]]),
                                "color"       : getattr(self.grid, row[col_idx["color"]]) if len(row[col_idx["color"]]) > 0 else None,
                                "img"         : getattr(self.grid.images, row[col_idx["img"]]) if len(row[col_idx["img"]]) > 0 else None,
                                "speed"       : int(float(row[col_idx["speed"]])) if len(row[col_idx["speed"]]) > 0 else None,
                                "range"       : int(float(row[col_idx["range"]])) if len(row[col_idx["range"]]) > 0 else None,
                                "time_color"  : getattr(self.grid, row[col_idx["time_color"]]) if len(row[col_idx["time_color"]]) > 0 else None,
                                "modable"     : bool(row[col_idx["modable"]]),
                                "collectible" : bool(row[col_idx["collectible"]]),
                                "consumable"  : bool(row[col_idx["consumable"]]),
                                "uses"        : int(float(row[col_idx["uses"]])) if len(row[col_idx["uses"]]) > 0 else 1,
                                "lifespan"    : float(row[col_idx["lifespan"]]) if len(row[col_idx["lifespan"]]) > 0 else None,
                                "vfreq"       : float(row[col_idx["vfreq"]]) if len(row[col_idx["vfreq"]]) > 0 else None,
                                "vspeed"      : int(float(row[col_idx["vspeed"]])) if len(row[col_idx["vspeed"]]) > 0 else 1,
                                "layer"       : int(float(row[col_idx["layer"]])) if len(row[col_idx["layer"]]) > 0 else 1,
                                "effects"     : str(row[col_idx["effects"]])
                            }
                        except Exception as e:
                            self.grid.msg(
                                'ERROR - Could not set attributes_dict {0}; klas: {1}; name: {2}'.format(
                                    e,
                                    klas,
                                    str(row[col_idx["name"]])))
                        # CREATE ITEM
                        result = None
                        if item_name:
                            try:
                                if item_name in attributes_dict["name"]:
                                    result = attributes_dict
                                else:
                                    continue
                            except Exception as e:
                                self.grid.msg("ERROR - Could not load item: %s" % e)
                                self.grid.msg("ERROR - item_name: %s" % item_name)
                                self.grid.msg("ERROR - attributes: %s" % attributes_dict)
                        else:
                            result = attributes_dict

                        yield result, klas

    def set_opts(self, item):
        options = item.options.split()
        item.options = {}
        for opt in options:
            for data, klas in self.load_data():
                if opt == data['name']:
                    opt_item = self.create_new_item(klas=klas,
                                                    attributes_dict=data)
                    item.options[opt_item.name] = opt_item
                    opt_item.available = True
                    if not opt_item.color:
                        opt_item.color = item.color
                    opt_item.default_color = item.color
                    setattr(opt_item, 'ober_item', item)

        if self.grid.show_debug:
            self.grid.msg("DEBUG - {0} options are: {1}".format(item.name, item.options))

    def set_timers(self, item):
        """ Set timers """
        if item.lifespan and isinstance(item.lifespan, (int, float)):
            lifespan = TimerItem()
            lifespan.radius = item.radius
            lifespan.default_radius = item.radius
            lifespan.duration = item.lifespan
            lifespan.limit = item.lifespan
            lifespan.color = item.time_color
            item.lifespan = lifespan

        if hasattr(item, "vfreq"):
            vibefr = TimerItem()
            vibefr.duration = item.vfreq
            vibefr.radius = item.radius
            vibefr.default_radius = item.radius
            if not hasattr(item, 'lifespan') or (hasattr(item, 'lifespan') and not item.lifespan):
                vibefr.color = item.time_color
            item.vfreq = vibefr
            if item.type in ['spawn']:
                item.vfreq.reversed = True

    def set_boost_timer(self, duration, effect, boosted_item, boost_item):

        boost_timer = TimerItem()
        boost_timer.duration = duration
        boost_timer.effects = effect
        setattr(boost_timer, 'boost_item', boost_item)
        setattr(boost_timer, 'store_color', boosted_item.default_color)
        if not hasattr(boosted_item, 'boost'):
            setattr(boosted_item, 'boost', list())
        boosted_item.boost.append(boost_timer)


    def load_item(self, item_name):
        new_item = None
        for data, klas in self.load_data(item_name):
            item = self.create_new_item(klas=klas,
                                        attributes_dict=data)
            if item.name == item_name:
                new_item = item
                self.set_timers(new_item)
                break
        if new_item:
            if new_item.options:
                self.set_opts(new_item)

        return new_item

    def set_door(self, item, room):
        door = Item()
        door.type = item.type
        door.name = "Enter_" + room
        door_room = item.name.replace("Enter_", "")
        door.pos = cu.get_mirror_point(item.pos, self.grid.center_tile)
        door.color = item.color
        if "door_enter" in item.type:
            door.img = self.grid.images.neon_exit
        else:
            door.img = item.img
        door.default_img = item.default_img
        door.default_color = item.color
        door.radius = item.radius
        door.default_radius = item.radius
        door.available = False

        self.set_timers(door)
        return door, door_room

    def set_buttons(self):
        """ Assign all items to the grid object """
        center = self.grid.find_center_tile()
        for name in ["play", "quit"]:
            # butt = ButtonItem()
            # butt.name = name
            # # butt.color = self.grid.room_color
            # butt.font = getattr(self.grid.fonts, 'small')
            # butt.text_color = self.grid.white

            butt = Item()
            butt.name = name
            # butt.color = self.grid.room_color

            if name == "play":
                butt.available = True
                butt.pos = self.grid.adj_tiles(center)[0]
                butt.img = self.grid.images.play
            elif name == "quit":
                butt.available = True
                butt.pos = self.grid.adj_tiles(center)[3]
                butt.img = self.grid.images.power


            self.grid.buttons.append(butt)

    def set_rooms(self):
        """
        Sets room items from hardcoded scenario conf
        :return:
        """
        if hasattr(self.grid, 'room_items'):
            for room in self.grid.room_items:
                for room_n, room_i in room.items():
                    if room_n not in self.grid.rooms.keys():
                        self.grid.rooms[room_n] = {
                            "items": [],
                            "revealed_tiles": {}
                        }
                    for candidate_item in room_i:
                        item_name = candidate_item["item_name"]
                        for pos in candidate_item["item_positions"]:
                            item = self.load_item(item_name)

                            try:
                                item.pos = self.grid.tile_dict[pos]
                            except Exception as e:
                                self.grid.msg(
                                    "ERROR - Set item: {0} \nin room: {1} \n{2} \n candidate: {3}".format(
                                        item, room_n, e, candidate_item))
                            if item.name in [xitem.name for xitem in self.grid.rooms[room_n]["items"]]:
                                item.name = item.name + '-' + str(time.time())
                                time.sleep(0.01)

                            if item.type in ["panel"]:
                                # INVENTORY
                                if item.name == "bag":
                                    i_pos_x = self.grid.rows - 1
                                    i_pos_y = self.grid.cols - 3
                                    i_pos = str(i_pos_x) + "_" + str(i_pos_y)
                                    item.pos = self.grid.names_to_pos(i_pos)
                                    item.available = True
                                    self.grid.panel_items['bag'] = item

                                # SLAB
                                elif item.name == 'slab':
                                    s_pos_x = self.grid.cols - 1
                                    s_pos_y = 3
                                    s_pos = str(s_pos_x) + "_" + str(s_pos_y)
                                    item.pos = self.grid.names_to_pos(s_pos)
                                    item.available = True
                                    setattr(self.grid, 'slab', item)
                                    self.grid.panel_items['slab'] = item

                            else:
                                self.grid.rooms[room_n]["items"].append(item)
                            # DOORS
                            if 'door' in item.type:
                                opposite_door, door_room_n = self.set_door(item, room_n)
                                if door_room_n not in self.grid.rooms.keys():
                                    self.grid.rooms[door_room_n] = {
                                        "items": [],
                                        "revealed_tiles": {}
                                    }
                                self.grid.rooms[door_room_n]["items"].append(opposite_door)

                            # MY BODY
                            elif item_name == "my_body":
                                item.available = True
                                item.gen_birth_track()
                                self.my_body = item

                            elif item.type in ['trigger']:
                                item.available = True


    def load_game(self):
        """
        Main loading execution of all items, res and preconditions
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
        self.grid.fog_color = getattr(self.grid, self.grid.fog_color)
        self.grid.room_color = getattr(self.grid, self.grid.room_color)

        self.grid.msg("INFO - Loading {0}".format(self.grid.scenario))
        self.set_rooms()
        self.set_buttons()

        self.my_body.inventory = self.grid.panel_items['bag']
        self.grid.items.append(self.my_body)

        self.grid.load_current_room()

        return self.my_body