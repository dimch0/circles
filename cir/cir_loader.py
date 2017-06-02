#######################################################################################################################
#################                                                                                     #################
#################                                    Loader                                           #################
#################                                                                                     #################
#######################################################################################################################
import csv

import cir_mobile
import cir_timer
import cir_button
import cir_item


def set_mode_vs_options(grid, mode_vs_options):
    """ Setting all options to item which have options """
    for item in grid.items:
        for mode_name, mode_options in mode_vs_options.items():

            if item.name == mode_name:
                item.default_options = mode_options
                item.options = item.default_options


def set_all_items(grid, all_items):
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


def load_all_items(grid, images, fonts, my_body):
    """
    This function loeads all items and menu options from external file.
    :return:  two dicts:
    ALL_ITEMS
    MODE_VS_OPTIONS
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
        for row in data:
            if not row[0] == "scenario":

                # ===================== COLS FROM data.csv FILE ==================== #
                item_scenario = row[0]
                item_category = row[1]
                item_type = row[2] if len(row[2]) > 0 else None
                item_name = row[3] if len(row[3]) > 0 else None
                item_pos = eval(row[4]) if len(row[4]) > 0 else ()
                item_color = getattr(grid, row[5]) if len(row[5]) > 0 else None
                item_img = getattr(images, row[6]) if len(row[6]) > 0 else None
                item_border = row[7] if len(row[7]) > 0 else 0
                item_speed = int(row[8]) if len(row[8]) > 0 else None
                item_range = row[9] if len(row[9]) > 0 else None
                item_font = getattr(fonts, row[10]) if len(row[10]) > 0 else None
                item_text_color = getattr(grid, row[11]) if len(row[11]) > 0 else None
                item_text = row[12] if len(row[12]) > 0 else None
                item_duration = int(row[13]) if len(row[13]) > 0 else None
                item_time_color = getattr(grid, row[14]) if len(row[14]) > 0 else None
                item_start_time = row[15] if len(row[15]) > 0 else None
                item_modable = row[16] if len(row[16]) > 0 else None
                # ===================== COLS FROM data.csv FILE ==================== #

                if item_scenario == "mode_vs_options":
                    item_to_append = cir_item.Item(
                        grid=grid,
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
                        item_to_append = cir_mobile.MobileItem(
                            grid=grid,
                            name=item_name,
                            pos=item_pos,
                            color=item_color,
                            speed=item_speed,
                            modable=item_modable
                        )
                        ALL_ITEMS[item_category].append(item_to_append)

                    elif item_type == "cir_timer":
                        item_to_append = cir_timer.TimerItem(
                            grid=grid,
                            name=item_name,
                            pos=item_pos,
                            color=item_color,
                            speed=item_speed,
                            duration=item_duration,
                            time_color=item_time_color,
                            modable=item_modable
                        )
                        ALL_ITEMS[item_category].append(item_to_append)

                    elif item_type == "cir_button":
                        item_to_append = cir_button.ButtonItem(
                            grid=grid,
                            name=item_name,
                            pos=item_pos,
                            color=item_color,
                            font=item_font,
                            text_color=item_text_color,
                            modable=item_modable
                        )
                        ALL_ITEMS[item_category].append(item_to_append)



    # Setting all items
    set_all_items(grid, ALL_ITEMS)

    # Setting the above mode options
    set_mode_vs_options(grid, MODE_VS_OPTIONS)

    return ALL_ITEMS, MODE_VS_OPTIONS


