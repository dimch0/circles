# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                                                                                     #
#                                                    Game Menu                                                        #
#                                                                                                                     #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #

def game_menu(grid, pygame):
    """ GAME MENU LOOP """
    while grid.game_menu:

        current_tile = grid.mouse_in_tile(pygame.mouse.get_pos())
        grid.seconds_in_game_tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                # --------------------------------------------------------------- #
                #                             'Escape'                            #
                # --------------------------------------------------------------- #
                if event.key == pygame.K_ESCAPE:
                    if grid.seconds_in_game > 0:
                        grid.game_menu = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_tile:
                    for button in grid.buttons:
                        if current_tile == button.pos and button.clickable:
                            if button.name in ["play", "replay"]:
                                grid.game_menu = False
                                if grid.game_over:
                                    grid.game_over = False
                            elif button.name == "quit":
                                pygame.quit()
                                quit()
        if grid.game_menu:
            if grid.buttons:
                grid.drawer.draw_menu_buttons(current_tile)
        pygame.display.update()