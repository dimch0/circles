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




def set_item_mode_options(grid, mode_vs_options):
    """
    Setting all options to grid.item
    mode_vs_options:
    """

    for item in grid.items:
        for mode_name, mode_options in mode_vs_options.items():

            if item.name == mode_name:
                item.default_options = mode_options
                item.options = item.default_options


def add_optoin_to_mode(category, item_obj, MODE_VS_OPTIONS):
    """ Appending the mode option to the MODE_VS_OPTIONS DICT """
    if category not in MODE_VS_OPTIONS.keys():
        MODE_VS_OPTIONS[category] = []
    MODE_VS_OPTIONS[category].append(item_obj)


def set_grid_items(grid, item):
    """ Assigning all items to the grid object """
    category = item['category']
    item_obj = item['object']
    grid.everything[item_obj.name] = item_obj

    if category == 'my body':
        if not item_obj in grid.bodies:
            grid.bodies.append(item_obj)
        if not item_obj in grid.items:
            grid.items.append(item_obj)
        return item_obj

    elif hasattr(grid, category):
        grid_attribute = getattr(grid, category)
        if not item_obj in grid_attribute:
            grid_attribute.append(item_obj)



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

    return dummy



def load_data(grid, images, fonts, SCENARIO):
    """
    This function loads all items and menu options from external data file.
    :param grid:  grid instance
    :param images:  images instance
    :param fonts:  fonts instance
    :param SCENARIO:  scenario number
    :return: a dict, containing the ITEM OBJECT, scenario, category and type
    """

    with open(grid.data_file, 'rb') as csvfile:

        data = csv.reader(csvfile, delimiter=',')
        HEADER = next(data)
        SCENARIO = SCENARIO
        print "Loading scenario...", SCENARIO

        # --------------------------------------------------------------- #
        #                        SET COLUMN INDEX                         #
        # --------------------------------------------------------------- #
        col_idx = {}
        for idx, name in enumerate(HEADER):
            col_idx[name] = idx

        for row in data:
            if not row == HEADER:

                # --------------------------------------------------------------- #
                #                      SET COLS AS ATTRIBUTES                     #
                # --------------------------------------------------------------- #
                scenario_col = row[col_idx["scenario"]]
                if str(SCENARIO) in scenario_col or "ALL" in scenario_col:
                    type = row[col_idx["type"]] if len(row[col_idx["type"]]) > 0 else None
                    category = row[col_idx["category"]]

                    attributes = {
                        "available"   : bool(row[col_idx["available"]]) if len(row[col_idx["available"]]) > 0 else None,
                        "border"      : row[col_idx["border"]] if len(row[col_idx["border"]]) > 0 else 0,
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
                    }

                    # --------------------------------------------------------------- #
                    #                         CREATING ITEM                           #
                    # --------------------------------------------------------------- #
                    ITEM_OBJECT = create_new_item(grid, type, attributes)

                    yield {
                        "object": ITEM_OBJECT,
                        "scenario": scenario_col,
                        "type": type,
                        "category": category
                    }


def load_items(grid, images, fonts, scenario):
    """
    Loading all grid items, my body and mode options
    :return: my_body, mode_vs_options
    """
    my_body = None
    mode_vs_options = {}

    for item in load_data(grid, images, fonts, scenario):

        category = item['category']
        item_obj = item['object']
        type = item["type"]

        if type == "mode_option":
            add_optoin_to_mode(category, item_obj, mode_vs_options)
        else:
            if category == "my body":
                my_body = set_grid_items(grid, item)
            else:
                set_grid_items(grid, item)

    # Setting mode_vs_options
    set_item_mode_options(grid, mode_vs_options)

    return my_body, mode_vs_options