
import cir_utils


def execute_key_events(grid, event, my_body):
    # --------------------------------------------------------------- #
    #                             ESCAPE                              #
    # --------------------------------------------------------------- #
    if event.key == grid.pygame.K_ESCAPE:
        if not grid.game_menu:
            grid.rename_button("replay", "play")
            grid.game_menu = True

    # --------------------------------------------------------------- #
    #                             SPACE                               #
    # --------------------------------------------------------------- #
    if event.key == grid.pygame.K_SPACE:

        # GEN RADAR
        my_body.gen_radar_track(grid)

        # DEBUG PRINT
        cir_utils.debug_print_space(grid, my_body)

    elif event.key == grid.pygame.K_KP_ENTER:
        for edit_btn in grid.editor_buttons:
            if not edit_btn in grid.items:
                grid.items.append(edit_btn)

    # --------------------------------------------------------------- #
    #                             NUMBERS                             #
    # --------------------------------------------------------------- #
    elif event.key == grid.pygame.K_1:
        print(">>>> key 1")
        grid.change_room("12_12")
    elif event.key == grid.pygame.K_2:
        print(">>>> key 2")
        grid.change_room("12_10")
    elif event.key == grid.pygame.K_3:
        print(">>>> key 3")
        grid.change_room("12_8")
    elif event.key == grid.pygame.K_4:
        print(">>>> key 4")
        grid.change_room("12_6")

    # --------------------------------------------------------------- #
    #                             OTHER                               #
    # --------------------------------------------------------------- #
    elif not my_body.in_menu:
        my_body.gen_direction(grid.pygame, grid, event)
