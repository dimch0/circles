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


def set_item_mode_options(grid):
    """
    Setting all options from grid.mode_vs_options to grid.items
    """
    for item in grid.items:
        for mode_name, mode_options in grid.mode_vs_options.items():

            if item.name == mode_name:
                item.default_options = mode_options
                item.options = item.default_options


def add_optoin_to_mode(category, item_obj, MODE_VS_OPTIONS):
    """ Appending the mode option to the MODE_VS_OPTIONS DICT """
    if category not in MODE_VS_OPTIONS.keys():
        MODE_VS_OPTIONS[category] = []
    MODE_VS_OPTIONS[category].append(item_obj)


def set_grid_items(grid, category, item):
    """ Assigning all items to the grid object """

    if category == 'my body':
        if not item in grid.items:
            grid.items.append(item)
        return item

    elif hasattr(grid, category):
        grid_attribute = getattr(grid, category)
        if not item in grid_attribute:
            grid_attribute.append(item)



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

    return dummy

def set_col_idx(header):
    """ Returns a dict with all columns as keys
    and their indexes as values """
    result = {}
    for idx, name in enumerate(header):
        result[name] = idx
    return result


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
                        "pos"         : eval(row[col_idx["pos"]]) if len(row[col_idx["pos"]]) > 0 else None,
                        "color"       : getattr(grid, row[col_idx["color"]]) if len(row[col_idx["color"]]) > 0 else None,
                        "img"         : getattr(images, row[col_idx["img"]]) if len(row[col_idx["img"]]) > 0 else None,
                        "speed"       : int(row[col_idx["speed"]]) if len(row[col_idx["speed"]]) > 0 else None,
                        "range"       : int(row[col_idx["range"]]) if len(row[col_idx["range"]]) > 0 else None,
                        "font"        : getattr(fonts, row[col_idx["font"]]) if len(row[col_idx["font"]]) > 0 else None,
                        "text_color"  : getattr(grid, row[col_idx["text_color"]]) if len(row[col_idx["text_color"]]) > 0 else None,
                        "duration"    : int(row[col_idx["duration"]]) if len(row[col_idx["duration"]]) > 0 else None,
                        "time_color"  : getattr(grid, row[col_idx["time_color"]]) if len(row[col_idx["time_color"]]) > 0 else None,
                        "modable"     : row[col_idx["modable"]] if len(row[col_idx["modable"]]) > 0 else None,
                        "collectable" : row[col_idx["collectable"]] if len(row[col_idx["collectable"]]) > 0 else None,
                        "uses"        : int(row[col_idx["uses"]]) if len(row[col_idx["uses"]]) > 0 else None
                    }
                    # Create an item
                    item = create_new_item(grid, type, attributes)
                    yield item, type, category


def load_items(grid, images, fonts, scenario):
    """
    Loading all grid items, my body and mode options
    :return: my_body
    """
    my_body = None
    for item, type, category in load_data(grid, images, fonts, scenario):
        # Everything
        grid.everything[item.name] = item
        # Mode options
        if type == "mode_option":
            add_optoin_to_mode(category, item, grid.mode_vs_options)
        else:
            # My body
            if category == "my body":
                my_body = set_grid_items(grid, category, item)
            else:
                set_grid_items(grid, category, item)
    # Setting mode_vs_options
    set_item_mode_options(grid)
    return my_body