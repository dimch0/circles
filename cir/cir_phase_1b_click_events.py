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
        if item.clickable:
            if current_tile == item.pos:

                # SET MOUSE MODE
                if item.modable:
                    grid.set_mouse_mode(item)

                # CLICK ON ITEMS
                grid.event_effects.click_items(item, my_body)

                # SET IN MENU OPTIONS
                item.check_in_menu(grid, current_tile)

                # SET OPTS POS
                item.set_option_pos(grid)

                # OPT CLICKED
                if item.in_menu:
                    grid.clean_mouse()

            # --------------------------------------------------------------- #
            #                       CLICK ON ITEM OPTIONS                     #
            # --------------------------------------------------------------- #
            elif current_tile in grid.adj_tiles(item.pos) and item.in_menu:
                if item.options:
                    for option in item.options:
                        if current_tile == option.pos:

                            # SET MOUSE MODE
                            if option.modable:
                                grid.set_mouse_mode(option)

                            # OPTIONS SUB-OPTIONS
                            grid.event_effects.click_options(item, option, my_body)

            # --------------------------------------------------------------- #
            #                          CLICKED OUTSIDE                        #
            # --------------------------------------------------------------- #
            else:
                item.set_in_menu(grid, False)

    # DEBUG PRINT
    cir_utils.debug_print_click(grid, current_tile, my_body)