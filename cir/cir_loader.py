#######################################################################################################################
#################                                                                                     #################
#################                                    Loader                                           #################
#################                                                                                     #################
#######################################################################################################################
import csv

import cir_item_mobile
import cir_item_timer
import cir_item_button
import cir_item


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


def set_all_grid_items(grid, all_items):
    """ Assigning all items to the grid object """
    # TODO: Parametrize scenario
    for category, items in all_items.items():
        for item in items:
            if category == "items":
                if not item in grid.items:
                    grid.items.append(item)
            elif category == "timers":
                if not item in grid.timers:
                    grid.timers.append(item)
            elif category == "buttons":
                if not item in grid.buttons:
                    grid.buttons.append(item)


def load_data(grid, images, fonts, my_body):
    """
    This function loads all items and menu options from external data file.
    :return:  two dicts:
    - ALL_ITEMS
    - MODE_VS_OPTIONS
    """
    ALL_ITEMS = {
        "items": [],
        "timers": [],
        "buttons": []
    }
    MODE_VS_OPTIONS = {
        "my body": [],
        "move": [],
        "sensory": [],
        "bokluk": [],
        "govna": []
    }

    with open(grid.data_file, 'rb') as csvfile:

        data = csv.reader(csvfile, delimiter=',')
        header = next(data)
        # --------------------------------------------------------------- #
        #                        SET COLUMN INDEX                         #
        # --------------------------------------------------------------- #
        for idx, name in enumerate(header):
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
            if not row[0] == "scenario":

                # --------------------------------------------------------------- #
                #                      SET COLS AS ATTRIBUTES                     #
                # --------------------------------------------------------------- #
                item_scenario = row[idx_scenario]
                item_category = row[idx_category]
                item_type = row[idx_type] if len(row[idx_type]) > 0 else None
                item_name = row[idx_name] if len(row[idx_name]) > 0 else None
                item_pos = eval(row[idx_pos]) if len(row[idx_pos]) > 0 else ()
                item_color = getattr(grid, row[idx_color]) if len(row[idx_color]) > 0 else None
                item_img = getattr(images, row[idx_img]) if len(row[idx_img]) > 0 else None
                item_border = row[idx_border] if len(row[idx_border]) > 0 else 0
                item_speed = int(row[idx_speed]) if len(row[idx_speed]) > 0 else None
                item_range = row[idx_range] if len(row[idx_range]) > 0 else None
                item_font = getattr(fonts, row[idx_font]) if len(row[idx_font]) > 0 else None
                item_text_color = getattr(grid, row[idx_text_color]) if len(row[idx_text_color]) > 0 else None
                item_text = row[idx_text] if len(row[idx_text]) > 0 else None
                item_duration = int(row[idx_duration]) if len(row[idx_duration]) > 0 else None
                item_time_color = getattr(grid, row[idx_time_color]) if len(row[idx_time_color]) > 0 else None
                item_modable = row[idx_modable] if len(row[idx_modable]) > 0 else None


                # --------------------------------------------------------------- #
                #                           CREATE ITEMS                          #
                # --------------------------------------------------------------- #
                if item_scenario == "mode_vs_options":
                    item_to_append = cir_item.Item(
                        name=item_name,
                        pos=item_pos,
                        color=item_color,
                        image=item_img,
                        border=item_border,
                        modable=item_modable
                    )
                    MODE_VS_OPTIONS[item_category].append(item_to_append)

                elif item_scenario == "scenario 1":
                    if item_type == "cir_mobile":
                        item_to_append = cir_item_mobile.MobileItem(
                            name=item_name,
                            pos=item_pos,
                            color=item_color,
                            speed=item_speed,
                            modable=item_modable
                        )
                        ALL_ITEMS[item_category].append(item_to_append)

                    elif item_type == "cir_timer":
                        item_to_append = cir_item_timer.TimerItem(
                            name=item_name,
                            pos=item_pos,
                            color=item_color,
                            speed=item_speed,
                            duration=item_duration,
                            time_color=item_time_color,
                            tile_radius=grid.tile_radius,
                            modable=item_modable
                        )
                        ALL_ITEMS[item_category].append(item_to_append)

                    elif item_type == "cir_button":
                        item_to_append = cir_item_button.ButtonItem(
                            name=item_name,
                            pos=item_pos,
                            color=item_color,
                            font=item_font,
                            text_color=item_text_color,
                            modable=item_modable
                        )
                        ALL_ITEMS[item_category].append(item_to_append)

    return ALL_ITEMS, MODE_VS_OPTIONS


def load_diskette(grid, images, fonts, my_body):

    ALL_ITEMS, MODE_VS_OPTIONS = load_data(grid, images, fonts, my_body)
    # Setting all items
    set_all_grid_items(grid, ALL_ITEMS)

    # Setting the above mode options
    set_mode_vs_options(grid, MODE_VS_OPTIONS)

    return ALL_ITEMS, MODE_VS_OPTIONS