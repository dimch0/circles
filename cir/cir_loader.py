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
            if not row[0] == "type":

                # ===================== COLS FROM data.csv FILE ==================== #
                item_type = row[0] if len(row[0]) > 0 else None
                item_name = row[1] if len(row[1]) > 0 else None
                item_pos = eval(row[2]) if len(row[2]) > 0 else ()
                item_color = getattr(grid, row[3]) if len(row[3]) > 0 else None
                item_img = getattr(images, row[4]) if len(row[4]) > 0 else None
                item_border = row[5] if len(row[5]) > 0 else 0
                item_speed = int(row[6]) if len(row[6]) > 0 else None
                item_range = row[7] if len(row[7]) > 0 else None
                item_font = getattr(fonts, row[8]) if len(row[8]) > 0 else None
                item_text_color = getattr(grid, row[9]) if len(row[9]) > 0 else None
                item_text = row[10] if len(row[10]) > 0 else None
                item_duration = int(row[11]) if len(row[11]) > 0 else None
                item_time_color = getattr(grid, row[12]) if len(row[12]) > 0 else None
                item_start_time = row[13] if len(row[13]) > 0 else None

                if item_type == "cir_mobile":
                    item_to_append = cir_mobile.MobileItem(
                        grid=grid,
                        name=item_name,
                        pos=item_pos,
                        color=item_color,
                        speed=item_speed
                    )
                    ALL_ITEMS["items"].append(item_to_append)

                elif item_type == "cir_timer":
                    item_to_append = cir_timer.TimerItem(
                        grid=grid,
                        name=item_name,
                        pos=item_pos,
                        color=item_color,
                        speed=item_speed,
                        duration=item_duration,
                        time_color=item_time_color
                    )
                    ALL_ITEMS["timers"].append(item_to_append)

                elif item_type == "cir_button":
                    item_to_append = cir_button.ButtonItem(
                        grid=grid,
                        name=item_name,
                        pos=item_pos,
                        color=item_color,
                        font=item_font,
                        text_color=item_text_color
                    )
                    ALL_ITEMS["buttons"].append(item_to_append)

                elif not "cir" in item_type:
                    item_to_append = cir_item.Item(
                        grid=grid,
                        name=item_name,
                        pos=item_pos,
                        color=item_color,
                        image=item_img,
                        border=item_border
                    )
                    MODE_VS_OPTIONS[item_type].append(item_to_append)

    return ALL_ITEMS, MODE_VS_OPTIONS