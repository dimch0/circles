# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                                                                                     #
#                                                    Game Menu                                                        #
#                                                                                                                     #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
def game_menu(grid, my_body, end_msg=''):
    """ GAME MENU LOOP """
    while grid.game_menu:

        current_tile = grid.mouse_in_tile(grid.pygame.mouse.get_pos())
        grid.seconds_in_game_tick()

        for event in grid.pygame.event.get():
            if event.type == grid.pygame.QUIT:
                grid.game_exit()

            elif event.type == grid.pygame.KEYDOWN:
                # --------------------------------------------------------------- #
                #                             'Escape'                            #
                # --------------------------------------------------------------- #
                if event.key == grid.pygame.K_ESCAPE:
                    if grid.seconds_in_game > 0:
                        grid.game_menu = False


            elif event.type == grid.pygame.MOUSEBUTTONDOWN:
                if current_tile:
                    for button in grid.buttons:
                        if current_tile == button.pos and button.clickable:
                            if button.name in ["play", "replay"]:
                                grid.game_menu = False
                                if grid.game_over:
                                    grid.game_over = False
                                if button.name == "replay":
                                    grid.messages = ["SCREEN - game started"]
                            elif button.name == "quit":
                                grid.game_exit()
        if grid.game_menu:
            if grid.buttons:
                grid.drawer.draw_menu_buttons(current_tile)
        grid.pygame.display.update()