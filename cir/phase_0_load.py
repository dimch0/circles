# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                   LOADER                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import csv
import time

import grid_util as cu

from circle import Circle
from circle_body import Body
from circle_door import Door
from circle_button import Button
from cir_room import Room


from grid_cosmetic import Images, Fonts, Colors
from phase_1_events import GameEvents
from phase_2_draw import GameDrawer
from phase_3_update import VarUpdater


class DataLoader(object):

    def __init__(self, grid=None):
        self.grid = grid
        self.csv_data = self.grid.data_file
        self.data_file = None
        self.mybody = None

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
        new_item = None
        try:
            if klas == "body":
                new_item = Body()
            elif klas == "item":
                new_item = Circle()
            elif klas == "door":
                new_item = Door()
        except Exception as e:
            self.grid.msg("ERROR - {0}, could not create item of klas: {1}".format(e, klas))

        try:
            for attribute, value in attributes_dict.items():
                if new_item and attribute:
                    if hasattr(new_item, attribute):
                        setattr(new_item, attribute, value)
                        if attribute == "time":
                            setattr(new_item, "max_time", value)


        except Exception as e:
            self.grid.msg("ERROR - Could not set attribute: {0}".format(e))

        try:
            new_item.radius = self.grid.tile_radius
        except Exception as e:
            self.grid.msg("ERROR - Could not set radius: %s" % e)
            self.grid.msg("ERROR - new_item: %s" % new_item)
            self.grid.msg("ERROR - klas: %s" % klas)
            self.grid.msg("ERROR - attributes: %s" % attributes_dict)

        # DEBUG
        if self.grid.show_debug:
           self.grid.msg("INFO - Loaded {0}".format(new_item.name))
           self.grid.msg("INFO - attributes_dict {0}".format(attributes_dict))

        return new_item

    def set_col_idx(self, header):
        """ Returns a dict with all columns as keys
        and their indexes as values """
        result = {}
        for idx, name in enumerate(header):
            result[name] = idx
        return result

    def set_color(self, color):
        result = None
        if hasattr(self.grid, color):
            result = getattr(self.grid, color)
        return result

    def set_img(self, image):
        result = None
        if hasattr(self.grid.images, image):
            result = getattr(self.grid.images, image)
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
                                "type"        : str(row[col_idx["type"]]) if len(row[col_idx["type"]]) > 0 else 'notype',
                                "name"        : str(row[col_idx["name"]]),
                                "lvl"         : str(row[col_idx["lvl"]]),
                                "color"       : self.set_color(row[col_idx["color"]]),
                                "img"         : self.set_img(row[col_idx["img"]]),
                                "time_color"  : self.set_color(row[col_idx["time_color"]]),
                                "modable"     : bool(row[col_idx["modable"]]),
                                "collectible" : bool(row[col_idx["collectible"]]),
                                "consumable"  : bool(row[col_idx["consumable"]]),
                                "time"        : int(row[col_idx["time"]]) if len(row[col_idx["time"]]) > 0 else None,
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
                            if not result:
                                self.grid.msg("ERROR - Could not find: %s" % (item_name))
                        else:
                            result = attributes_dict

                        yield result, klas

    def load_item(self, item_name):
        new_item = None
        for data, klas in self.load_data(item_name):
            item = self.create_new_item(klas=klas,
                                        attributes_dict=data)
            if item.name == item_name:
                new_item = item
                break

        if not new_item:
            self.grid.msg('ERROR - Failed to load item: %s' % item_name)

        return new_item


    def set_buttons(self):
        """ Assign all items to the grid object """
        center = self.grid.find_center_tile()
        for name in ["play", "quit"]:
            butt = Button()
            butt.name = name
            butt.type = 'button'
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
                        self.grid.rooms[room_n] = Room()

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
                            if item.name in [xitem.name for xitem in self.grid.rooms[room_n].circles]:
                                item.name = item.name + '-' + str(time.time())
                                time.sleep(0.01)
                            else:
                                self.grid.rooms[room_n].circles.append(item)

                            # MY BODY
                            if item_name == "mybody":
                                item.available = True
                                item.gen_birth_track()
                                self.mybody = item


    def load_game(self):
        """
        Main loading execution of all items, res and preconditions
        :return: mybody
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
        self.grid.color1 = getattr(self.grid, self.grid.color1)

        self.grid.msg("INFO - Loading {0}".format(self.grid.scenario))
        self.set_rooms()
        self.set_buttons()

        self.grid.circles.append(self.mybody)

        self.grid.load_current_room()
        self.mybody.gen_vibe_track(self.grid)
        return self.mybody