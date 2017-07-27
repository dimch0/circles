#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                                    Loader                                           #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
import csv
import cir_item
import cir_item_body
import cir_item_timer
import cir_item_button
import cir_item_mobile


def create_new_item(grid, type, attributes):
    """
    This function creates an item of a class by the given type.
    Attributes are set by a given dict (attributes)
    :param grid: grid instance
    :param type: type specified
    :param attributes: generated dict
    :return: a new instance of an item object
    """
    dummy = None
    try:
        if type == "body":
            dummy = cir_item_body.BodyItem()
        elif type == "timer":
            dummy = cir_item_timer.TimerItem()
            dummy.timer_tile_radius = grid.tile_radius
        elif type == "button":
            dummy = cir_item_button.ButtonItem()
        elif type == "mobile":
            dummy = cir_item_mobile.MobileItem()
        elif type in ["mode_option", "simple"]:
            dummy = cir_item.Item()
    except Exception as e:
        print e
        print "Error, could not create item of type: {0}".format(type)

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

    dummy.radius = grid.tile_radius
    return dummy

def set_col_idx(header):
    """ Returns a dict with all columns as keys
    and their indexes as values """
    result = {}
    for idx, name in enumerate(header):
        result[name] = idx
    return result


def set_pos(grid, number):
    """
    Calculate the position as following:
    The number is split to a list of digits
    The first digit is always 1 - that is the center tile
    Each digit after it is the index of an adjacent tile to the previous tile
    :param grid: grid instance
    :param number: column value
    :return: the final position
    """
    position = None
    indexes = [int(n) for n in number]
    if indexes:
        position = grid.center_tile
    if len(indexes) > 1:
        for idx in indexes[1:]:
            position = grid.adj_tiles(position)[idx]
    return position

def load_data(grid, images, fonts, SCENARIO):
    """
    This function loads all items and menu options from external data file.
    :param grid:  grid instance
    :param images:  images instance
    :param fonts:  fonts instance
    :param SCENARIO:  scenario number
    :return: item object, type and category
    """
    print "Loading", SCENARIO, "..."
    with open(grid.data_file, 'rb') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        header = next(data)
        col_idx = set_col_idx(header)
        for row in data:
            if not row == header:
                scenario_col = row[col_idx["scenario"]]
                if str(SCENARIO) in scenario_col or "ALL" in scenario_col:
                    category = row[col_idx["category"]]
                    type = row[col_idx["type"]]
                    # --------------------------------------------------------------- #
                    #                        ATTRIBUTES DICT                          #
                    # --------------------------------------------------------------- #
                    attributes = {
                        "available"   : bool(row[col_idx["available"]]) if len(row[col_idx["available"]]) > 0 else None,
                        "border"      : row[col_idx["border"]] if len(row[col_idx["border"]]) > 0 else 0,
                        "border_width": int(row[col_idx["border_width"]]) if len(row[col_idx["border_width"]]) > 0 else 1,
                        "border_color": getattr(grid, row[col_idx["border_color"]]) if len(row[col_idx["border_color"]]) > 0 else None,
                        "name"        : row[col_idx["name"]] if len(row[col_idx["name"]]) > 0 else None,
                        "pos"         : set_pos(grid, row[col_idx["pos"]]) if len(row[col_idx["pos"]]) > 0 else None,
                        "color"       : getattr(grid, row[col_idx["color"]]) if len(row[col_idx["color"]]) > 0 else None,
                        "img"         : getattr(images, row[col_idx["img"]]) if len(row[col_idx["img"]]) > 0 else None,
                        "speed"       : int(row[col_idx["speed"]]) if len(row[col_idx["speed"]]) > 0 else None,
                        "range"       : int(row[col_idx["range"]]) if len(row[col_idx["range"]]) > 0 else None,
                        "font"        : getattr(fonts, row[col_idx["font"]]) if len(row[col_idx["font"]]) > 0 else None,
                        "text_color"  : getattr(grid, row[col_idx["text_color"]]) if len(row[col_idx["text_color"]]) > 0 else None,
                        "time_color"  : getattr(grid, row[col_idx["time_color"]]) if len(row[col_idx["time_color"]]) > 0 else None,
                        "modable"     : row[col_idx["modable"]] if len(row[col_idx["modable"]]) > 0 else None,
                        "collectable" : row[col_idx["collectable"]] if len(row[col_idx["collectable"]]) > 0 else None,
                        "uses"        : int(row[col_idx["uses"]]) if len(row[col_idx["uses"]]) > 0 else None,
                        "room"        : int(row[col_idx["room"]]) if len(row[col_idx["room"]]) > 0 else None,
                        "lifespan"    : float(row[col_idx["lifespan"]]) if len(row[col_idx["lifespan"]]) > 0 else None,
                    }
                    # Create an item
                    item = create_new_item(grid, type, attributes)
                    yield item, type, category


def add_optoin_to_mode(grid, category, option):
    """ Append the mode option to the MODE_VS_OPTIONS DICT """
    if category not in grid.mode_vs_options.keys():
        grid.mode_vs_options[category] = []
    grid.mode_vs_options[category].append(option)


def set_mode_options(grid):
    """ Assign all options from grid.mode_vs_options to grid.items """
    for name, item in grid.everything.items():
        for mode_name, mode_options in grid.mode_vs_options.items():
            if item.name == mode_name:
                item.default_options = mode_options
                item.options = item.default_options


def set_timers(grid):
    """ Assign all options from grid.mode_vs_options to grid.items """
    for name, item in grid.everything.items():

        if item.lifespan:
            timer = cir_item_timer.TimerItem()
            timer.timer_tile_radius = grid.tile_radius
            timer.duration = item.lifespan
            timer.color = item.time_color
            item.lifespan = timer

        if item.birth_time:
            timer = cir_item_timer.TimerItem()
            timer.duration = item.birth_time
            item.birth_time = timer


def set_buttons(grid, category, item):
    """ Assign all items to the grid object """
    if category == "buttons":
        grid_attribute = getattr(grid, category)
        if not item in grid_attribute:
            grid_attribute.append(item)


def set_rooms(grid, item):
    if item.room not in [None, ""]:
        if item.room not in grid.rooms.keys():
            grid.rooms[item.room] = {
                "items"          : [],
                "revealed_radius": []
            }
        grid.rooms[item.room]["items"].append(item)


def load_items(grid, images, fonts, scenario):
    """
    Loading all modes, buttons, timers, my_body
    :return: my_body
    """
    for item, type, category in load_data(grid, images, fonts, scenario):
        # Everything
        grid.everything[item.name] = item
        set_rooms(grid, item)
        # Mode options
        if type == "mode_option":
            add_optoin_to_mode(grid, category, item)
        # Buttons
        else:
            set_buttons(grid, category, item)

    set_mode_options(grid)
    set_timers(grid)
    my_body = grid.everything["my_body"]
    my_body.gen_birth_track()
    grid.rooms[grid.current_room]["revealed_radius"].append(((my_body.pos), grid.tile_radius))
    grid.load_current_room()

    return my_body