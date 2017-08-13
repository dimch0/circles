import cir_utils

def execute_click_events(grid, event, my_body, current_tile):


    # --------------------------------------------------------------- #
    #                         MOUSE MODE CLICK                        #
    # --------------------------------------------------------------- #
    grid.event_effects.mouse_mode_click(current_tile, my_body)

    # --------------------------------------------------------------- #
    #                          CLICK ON ITEMS                         #
    # --------------------------------------------------------------- #
    for item in grid.items:
        if item.clickable and item.available:
            if current_tile == item.pos:

                if item.type == "option":
                    oitem = item.get_ober_item(grid)
                    oitem.close_menu(grid)

                if item.in_menu:
                    if not item.mode:
                        item.close_menu(grid)
                    else:
                        item.revert_menu(grid)

                elif item.has_opts and not item.in_menu:
                    item.open_menu(grid)

                # SET MOUSE MODE
                if item.modable:
                    grid.set_mouse_mode(item)

                # CLICK ON ITEMS
                grid.event_effects.click_items(item, my_body)

                # CLEAN MOUSE
                if item.in_menu:
                    grid.clean_mouse()
            # MENU OFF
            elif current_tile not in grid.adj_tiles(item.pos):
                if item.in_menu:
                    item.close_menu(grid)

            # # --------------------------------------------------------------- #
            # #                       CLICK ON ITEM OPTIONS                     #
            # # --------------------------------------------------------------- #
            # elif current_tile in grid.adj_tiles(item.pos) and item.in_menu:
            #     if item.options:
            #         for option in item.options:
            #             if current_tile == option.pos:
            #
            #                 # SET MOUSE MODE
            #                 if option.modable:
            #                     grid.set_mouse_mode(option)
            #
            #                 # OPTIONS SUB-OPTIONS
            #                 grid.event_effects.click_options(item, option, my_body)
            #
            # # --------------------------------------------------------------- #
            # #                          CLICKED OUTSIDE                        #
            # # --------------------------------------------------------------- #
            # else:
            #     item.set_in_menu(grid, False)

    # DEBUG PRINT
    cir_utils.debug_print_click(grid, current_tile, my_body)