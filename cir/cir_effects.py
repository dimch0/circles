#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                                        Effects                                      #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
import copy
import random

# --------------------------------------------------------------- #
#                                                                 #
#                         BASIC EFFECTS                           #
#                                                                 #
# --------------------------------------------------------------- #
def produce(grid, product, position):
    """
    Produces an item from the everything dict
    :param grid: grid instance
    :param product: name of the item from the everything dict
    :param position: new position
    :return: the new item
    """
    produced_item = None
    for name, item in grid.everything.items():
        if name == product:
            produced_item = copy.deepcopy(item)
            produced_item.img = item.img
            produced_item.default_img = item.default_img
            produced_item.pos = position
            produced_item.available = True
            produced_item.gen_birth_track(grid)
            grid.items.append(produced_item)
    return produced_item


# --------------------------------------------------------------- #
#                                                                 #
#                         MOUSE MODES                             #
#                                                                 #
# --------------------------------------------------------------- #
def laino_mode_click(grid, current_tile):
    """
    For mode 'laino', if clicked produces an item
    :param grid: grid instance
    :param current_tile: the clicked circle
    """
    if current_tile not in grid.occupado_tiles and current_tile in grid.revealed_tiles:
        produce(grid, "shit", current_tile)


def shit_mode_click(grid, current_circle):
    """
    For mode 'shit', if clicked produces an item and exhausts mode uses
    :param grid: grid instance
    :param current_circle: the clicked circle
    """
    for bag_item in grid.mode_vs_options["bag"]:
        if bag_item.name == grid.mouse_mode:
            if bag_item.uses:
                if current_circle not in grid.occupado_tiles: #and current_circle in grid.revealed_tiles:
                    produce(grid, "shit", current_circle)
                    bag_item.uses -= 1
                    return 1


# --------------------------------------------------------------- #
#                                                                 #
#                           BAG MODES                             #
#                                                                 #
# --------------------------------------------------------------- #
def collect(grid, item):
    """ Collect item: add it to bag options """
    if item.collectable:
        for option in grid.mode_vs_options["bag"]:
            if "bag_placeholder" in option.name:
                grid.mode_vs_options["bag"].remove(option)
                new_item = copy.deepcopy(item)
                new_item.modable = True
                new_item.img = item.img
                new_item.default_img = item.default_img
                new_item.color = item.color
                grid.mode_vs_options["bag"].append(new_item)
                item.available = False
                grid.items.remove(item)
                return 1


def empty_bag(grid):
    """ Empties the bag if an item's uses are exhausted """
    for bag_item in grid.mode_vs_options["bag"]:
        if bag_item.uses == 0:
            grid.mode_vs_options["bag"].remove(bag_item)
            empty_placeholder = copy.deepcopy(grid.everything["bag_placeholder"])
            empty_placeholder.color = grid.everything["bag_placeholder"].color
            grid.mode_vs_options["bag"].append(empty_placeholder)
            if grid.mouse_mode == bag_item.name:
                grid.clean_mouse()
            return 1


# --------------------------------------------------------------- #
#                                                                 #
#                       ENTER / EXIT EFFECTS                      #
#                                                                 #
# --------------------------------------------------------------- #
def enter_exit(grid, my_body, item, option):
    """
    Changes the current room
    :param grid: grid instance
    :param my_body: my_body instance
    :param item: enter / exit item
    :param option: option of the above item -> holds the room number
    """
    room_number = None

    if "enter_" in option.name:
        room_number = option.name.replace("enter_", "")
        room_number = int(room_number)
    elif "exit_" in option.name:
        room_number = option.name.replace("exit_", "")
        room_number = int(room_number)

    if my_body.pos in grid.adj_tiles(item.pos) and room_number:
        my_body.move_track = my_body.move_to_tile(grid, item.pos)
        grid.change_room(room_number)
    else:
        print "it far"


# --------------------------------------------------------------- #
#                                                                 #
#                         TIMER EFFECTS                           #
#                                                                 #
# --------------------------------------------------------------- #
def birth_time_over_effect(item):
    """ Birth timer effect """
    if item.birth_track:
        item.birth_track.pop(0)
        item.birth_time.restart()

# lifespan
def my_body_lifespan_over_effect(grid):
    grid.game_over = True

# observer
def observer_lifespan_over_effect(grid, item):
    if not item.move_track:
        item.gen_radar_track(grid)

    if len(item.radar_track) == 1:
        legal_moves = []
        for item_adj in grid.adj_tiles(item.pos):
            if item_adj in grid.playing_tiles and item_adj not in grid.occupado_tiles:
                legal_moves.append(item_adj)

        if legal_moves:
            # item.move_track = item.move_to_tile(grid, item.pos, random.choice(legal_moves))
            item.move_track = item.move_to_tile(grid, random.choice(legal_moves))
            item.lifespan.restart()


def timer_effect(grid, item):
    """ Timer effects  """
    if item.lifespan:
        item.lifespan.tick()

        if item.lifespan.is_over:
            if item.name == "my_body":
                my_body_lifespan_over_effect(grid)
            elif item.name == "observer":
                observer_lifespan_over_effect(grid, item)

    if item.birth_time:
        item.birth_time.tick()
        if item.birth_time.is_over:
            # print item.name, item.birth_time.duration
            birth_time_over_effect(item)


# --------------------------------------------------------------- #
#                        MOUSE MODE CLICK                         #
# --------------------------------------------------------------- #
def mouse_mode_click(grid, current_tile):
    if grid.mouse_mode == "laino":
        laino_mode_click(grid, current_tile)
    elif grid.mouse_mode == "shit":
        shit_mode_click(grid, current_tile)
    elif grid.mouse_mode == "see":
        if current_tile not in grid.occupado_tiles and current_tile in grid.revealed_tiles:
            produce(grid, "observer", current_tile)
            # TODO fix below line
            # grid.everything["observer"].lifespan.restart()


# --------------------------------------------------------------- #
#                    MOUSE MODE CLICK ON ITEM                     #
# --------------------------------------------------------------- #
def mouse_mode_click_item(grid, item):
    if grid.mouse_mode == "bag":
        collect(grid, item)


def click_options(grid, item, option, my_body):
    # --------------------------------------------------------------- #
    #                       CLICK DEFAULT OPTIONS                     #
    # --------------------------------------------------------------- #
    if option in item.default_options:
        # bag
        if option.name == "bag":
            print "Gimme the loot!"
        # mitosis
        elif option.name == "mitosis":
            item.mitosis(grid)
        # enter / exit
        elif any(a for a in ["enter_", "exit_"] if a in option.name):
            enter_exit(grid, my_body, item, option)

        # Setting the mode
        item.set_mode(grid, option)

    # --------------------------------------------------------------- #
    #                        CLICK SUB-OPTIONS                        #
    # --------------------------------------------------------------- #
    elif option in grid.mode_vs_options[item.mode]:
        # move
        if item.mode == "move":
            item.gen_move_track(grid, grid.mode_vs_options[item.mode].index(option))
        # see
        elif option.name == "see":
            # item.range += 3
            print "seen"
        # smel
        elif option.name == "smel":
            print "sniff hair"
        # medi
        elif option.name == "medi":
            item.range += 3
            my_body.gen_radar_track(grid)
            item.range -= 3
        # audio
        elif option.name == "audio":
            item.range += 1
        # eat
        elif option.name == "eat":
            item.change_speed(-1)
        # touch
        elif option.name == "touch":
            item.change_speed(1)
        # Close menu when sub-option selected
        item.set_in_menu(grid, False)
    # Close menu if option has no sub-options
    if option.name not in grid.mode_vs_options.keys():
        item.set_in_menu(grid, False)