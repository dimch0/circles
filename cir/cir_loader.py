#######################################################################################################################
#################                                                                                     #################
#################                                    Loader                                           #################
#################                                                                                     #################
#######################################################################################################################
import csv
import sys
import cir_item
import cir_item_body
import cir_item_timer
import cir_item_button
import cir_item_mobile



def set_mode_vs_options(grid, mode_vs_options):
    """
    Setting all options to grid.item
    mode_vs_options:
    """

    for item in grid.items:
        for mode_name, mode_options in mode_vs_options.items():

            if item.name == mode_name:
                item.default_options = mode_options
                item.options = item.default_options



def get_mode_vs_options(category, item_obj, MODE_VS_OPTIONS):
    if category not in MODE_VS_OPTIONS.keys():
        MODE_VS_OPTIONS[category] = []
    MODE_VS_OPTIONS[category].append(item_obj)




def set_grid_items(grid, item):
    """ Assigning all items to the grid object """
    category = item['category']
    item_obj = item['object']

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


def create_item(type, attribute):
    print "DEBUG", type
    dummy = eval(type + "()")
    print(vars(dummy))

    if attribute in vars(dummy).keys():
        print attribute
    sys.exit()



def load_data(grid, images, fonts, SCENARIO):
    """
    This function loads all items and menu options from external data file.
    :return:  two dicts:
    - ALL_ITEMS
    - MODE_VS_OPTIONS
    """


    with open(grid.data_file, 'rb') as csvfile:

        data = csv.reader(csvfile, delimiter=',')
        HEADER = next(data)
        ITEM_OBJECT = None
        SCENARIO = SCENARIO

        # --------------------------------------------------------------- #
        #                        SET COLUMN INDEX                         #
        # --------------------------------------------------------------- #
        for idx, name in enumerate(HEADER):
            if name == "scenario":
                idx_scenario = idx
            elif name == "category":
                idx_category = idx
            elif name == "type":
                idx_type = idx
            elif name == "name":
                idx_name = idx
            elif name == "pos":
                idx_pos = idx
            elif name == "color":
                idx_color = idx
            elif name == "img":
                idx_img = idx
            elif name == "border":
                idx_border = idx
            elif name == "speed":
                idx_speed = idx
            elif name == "range":
                idx_range = idx
            elif name == "font":
                idx_font = idx
            elif name == "text_color":
                idx_text_color = idx
            elif name == "text":
                idx_text = idx
            elif name == "duration":
                idx_duration = idx
            elif name == "time_color":
                idx_time_color = idx
            elif name == "modable":
                idx_modable = idx

        for row in data:
            if not row == HEADER:
                # --------------------------------------------------------------- #
                #                      SET COLS AS ATTRIBUTES                     #
                # --------------------------------------------------------------- #
                item_scenario = row[idx_scenario]
                if str(SCENARIO) in item_scenario or "ALL" in item_scenario:
                    type = row[idx_type] if len(row[idx_type]) > 0 else None
                    category = row[idx_category]
                    attributes = {
                        "name": row[idx_name] if len(row[idx_name]) > 0 else None,
                        "pos": eval(row[idx_pos]) if len(row[idx_pos]) > 0 else (),
                        "color": getattr(grid, row[idx_color]) if len(row[idx_color]) > 0 else None,
                        "img": getattr(images, row[idx_img]) if len(row[idx_img]) > 0 else None,
                        "border": row[idx_border] if len(row[idx_border]) > 0 else 0,
                        "speed": int(row[idx_speed]) if len(row[idx_speed]) > 0 else None,
                        "range": int(row[idx_range]) if len(row[idx_range]) > 0 else None,
                        "font": getattr(fonts, row[idx_font]) if len(row[idx_font]) > 0 else None,
                        "text_color": getattr(grid, row[idx_text_color]) if len(row[idx_text_color]) > 0 else None,
                        "text": row[idx_text] if len(row[idx_text]) > 0 else None,
                        "duration": int(row[idx_duration]) if len(row[idx_duration]) > 0 else None,
                        "time_color": getattr(grid, row[idx_time_color]) if len(row[idx_time_color]) > 0 else None,
                        "modable": row[idx_modable] if len(row[idx_modable]) > 0 else None,
                    }

                    # print attributes
                    for attr in attributes.keys():
                        create_item(type, attr)


                    # item_category = row[idx_category]
                    # item_type = row[idx_type] if len(row[idx_type]) > 0 else None
                    # item_name = row[idx_name] if len(row[idx_name]) > 0 else None
                    # item_pos = eval(row[idx_pos]) if len(row[idx_pos]) > 0 else ()
                    # item_color = getattr(grid, row[idx_color]) if len(row[idx_color]) > 0 else None
                    # item_img = getattr(images, row[idx_img]) if len(row[idx_img]) > 0 else None
                    # item_border = row[idx_border] if len(row[idx_border]) > 0 else 0
                    # item_speed = int(row[idx_speed]) if len(row[idx_speed]) > 0 else None
                    # item_range = int(row[idx_range]) if len(row[idx_range]) > 0 else None
                    # item_font = getattr(fonts, row[idx_font]) if len(row[idx_font]) > 0 else None
                    # item_text_color = getattr(grid, row[idx_text_color]) if len(row[idx_text_color]) > 0 else None
                    # item_text = row[idx_text] if len(row[idx_text]) > 0 else None
                    # item_duration = int(row[idx_duration]) if len(row[idx_duration]) > 0 else None
                    # item_time_color = getattr(grid, row[idx_time_color]) if len(row[idx_time_color]) > 0 else None
                    # item_modable = row[idx_modable] if len(row[idx_modable]) > 0 else None

                    # --------------------------------------------------------------- #
                    #                           CREATE ITEMS                          #
                    # --------------------------------------------------------------- #
                    # TODO: Create a function that checks which attributes are needed


                    if item_type == "my_body":
                        ITEM_OBJECT = cir_item_body.BodyItem(
                            name=item_name,
                            pos=item_pos,
                            color=item_color,
                            image=item_img,
                            speed=item_speed,
                            range=item_range,
                            border=item_border,
                            modable=item_modable
                        )

                    elif item_type == "mode_option":
                        ITEM_OBJECT = cir_item.Item(
                            name=item_name,
                            pos=item_pos,
                            color=item_color,
                            image=item_img,
                            border=item_border,
                            modable=item_modable
                        )

                    elif item_type == "cir_mobile":
                        ITEM_OBJECT = cir_item_mobile.MobileItem(
                            name=item_name,
                            pos=item_pos,
                            color=item_color,
                            speed=item_speed,
                            modable=item_modable
                        )

                    elif item_type == "cir_timer":
                        ITEM_OBJECT = cir_item_timer.TimerItem(
                            name=item_name,
                            pos=item_pos,
                            color=item_color,
                            speed=item_speed,
                            duration=item_duration,
                            time_color=item_time_color,
                            tile_radius=grid.tile_radius,
                            modable=item_modable
                        )

                    elif item_type == "cir_button":
                        ITEM_OBJECT = cir_item_button.ButtonItem(
                            name=item_name,
                            pos=item_pos,
                            color=item_color,
                            font=item_font,
                            text_color=item_text_color,
                            modable=item_modable
                        )

                    yield {
                        "object": ITEM_OBJECT,
                        "scenario": item_scenario,
                        "type": item_type,
                        "category": item_category
                    }


