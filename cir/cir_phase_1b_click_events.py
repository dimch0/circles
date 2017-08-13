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
                print("Clicked item: {0}".format(item.name))

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
                    my_body.mode = item.name

                # CLICK ON ITEMS
                grid.event_effects.click_items(item, my_body)


                # CLEAN MOUSE
                if item.in_menu:
                    grid.clean_mouse()
            # MENU OFF
            elif current_tile not in grid.adj_tiles(item.pos):
                if item.in_menu:
                    item.close_menu(grid)



    # DEBUG PRINT
    cir_utils.debug_print_click(grid, current_tile, my_body)