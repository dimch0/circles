#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                                        Effects                                      #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
import copy
import random
import cir_utils

# --------------------------------------------------------------- #
#                                                                 #
#                         BASIC EFFECTS                           #
#                                                                 #
# --------------------------------------------------------------- #
def produce(grid, product, pos, radius=None, birth=None):
    """
    Produces an item from the everything dict
    :param grid: grid instance
    :param product: name of the item from the everything dict
    :param pos: new position
    :return: the new item
    """
    produced_item = None
    for name, item in grid.everything.items():
        if name == product:
            if radius:
                item.radius = radius
            if birth:
                item.birth_time.duration = birth
            produced_item = copy.deepcopy(item)
            produced_item.img = item.img
            produced_item.default_img = item.default_img
            produced_item.pos = pos
            produced_item.available = True
            produced_item.gen_birth_track()
            grid.items.append(produced_item)
    return produced_item


def destroy(grid, item):
    if item in grid.items and not item.name == "my_body" and not item.birth_track:
        item.in_menu = False
        item.gen_birth_track()
        item.birth_track.reverse()
        item.needs_to_be_destroyed = True




def destruction(grid, item):
    if item.needs_to_be_destroyed and not item.birth_track:
        # Signal
        if item.name == "signal":
            if not item.move_track:
                item.available = False
                grid.items.remove(item)
        else:
            item.available = False
            grid.items.remove(item)




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


def eat_mode_effect(grid, current_tile):
    """ Eat that shit """
    for item in grid.items:
        if current_tile == item.pos:
            destroy(grid, item)


def echo_mode_effect(grid, current_tile, my_body):
    """ Signal effect """
    signal = produce(grid,
                     "signal",
                     my_body.pos,
                     radius = 8,
                     birth = 0)

    target_tile = cir_utils.get_mirror_point(current_tile, my_body.pos)
    signal.move_track = signal.move_to_tile(grid, target_tile)



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
def enter_room(grid, my_body, item):
    if "Exit_" in item.name or "Enter_" in item.name:
        room_number = None
        for option in item.options:
            if "Enter_" in option.name:
                room_number = option.name.replace("Enter_", "")
                room_number = int(room_number)

        if my_body.pos == item.pos and grid.needs_to_change_room:
            grid.change_room(room_number)
            my_body.available = True
            my_body.gen_birth_track()
            grid.rooms[grid.current_room]["revealed_radius"].append(((item.pos), grid.tile_radius))


def exit_room(grid, my_body, item):
    """
    Changes the current room
    :param grid: grid instance
    :param my_body: my_body instance
    :param item: enter / exit item
    :param option: option of the above item -> holds the room number
    """
    if my_body.pos in grid.adj_tiles(item.pos):
        my_body.move_track = my_body.move_to_tile(grid, item.pos)
        grid.needs_to_change_room = True
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
            item.move_track = item.move_to_tile(grid, random.choice(legal_moves))
            item.lifespan.restart()


def signal_lifespan_over_effect(grid, item):
    print item.birth_track
    destroy(grid, item)


    # def destroy(grid, item):
    #     if item in grid.items and not item.name == "my_body":
    #         item.in_menu = False
    #         item.gen_birth_track()
    #         item.birth_track.reverse()
    #         item.needs_to_be_destroyed = True


def timer_effect(grid, item):
    """ Timer effects  """
    if item.lifespan:
        item.lifespan.tick()

        if item.lifespan.is_over:
            if item.name == "my_body":
                my_body_lifespan_over_effect(grid)
            elif item.name == "observer":
                observer_lifespan_over_effect(grid, item)
            elif item.name == "signal":
                signal_lifespan_over_effect(grid, item)

    if item.birth_track:
        if item.birth_time and not isinstance(item.birth_time, float):
            item.birth_time.tick()
            if item.birth_time.is_over:
                birth_time_over_effect(item)


# --------------------------------------------------------------- #
#                        MOUSE MODE CLICK                         #
# --------------------------------------------------------------- #
def mouse_mode_click(grid, current_tile, my_body):
    if grid.mouse_mode == "laino":
        laino_mode_click(grid, current_tile)
    elif grid.mouse_mode == "shit":
        shit_mode_click(grid, current_tile)
    elif grid.mouse_mode == "see":
        if current_tile not in grid.occupado_tiles and current_tile in grid.revealed_tiles:
            new_observer = produce(grid, "observer", current_tile)
            new_observer.lifespan.restart()
    elif grid.mouse_mode == "eat":
        eat_mode_effect(grid, current_tile)
    elif grid.mouse_mode == "echo":
        echo_mode_effect(grid, current_tile, my_body)

# --------------------------------------------------------------- #
#                    MOUSE MODE CLICK ON ITEM                     #
# --------------------------------------------------------------- #
def mouse_mode_click_item(grid, item):
    if grid.mouse_mode == "bag":
        collect(grid, item)


# --------------------------------------------------------------- #
#                                                                 #
#                            BODY MODES                           #
#                                                                 #
# --------------------------------------------------------------- #
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

        elif option.name == "move":
            item.change_speed(0.1)

        elif option.name == "echo":
            # activate signal mode
            item.change_speed(0.1)

        # enter / exit
        elif "Enter_" in option.name:
            exit_room(grid, my_body, item)

        # Setting the mode
        item.set_mode(grid, option)

    # --------------------------------------------------------------- #
    #                        CLICK SUB-OPTIONS                        #
    # --------------------------------------------------------------- #
    elif option in grid.mode_vs_options[item.mode]:
        # see
        if option.name == "see":
            print "Seen"

        # smel
        elif option.name == "smel":
            print "Sniff hair"

        # medi
        elif option.name == "medi":
            print "Ommmm"
            item.range += 3
            my_body.gen_radar_track(grid)
            item.range -= 3

        # audio
        elif option.name == "audio":
            print "Who"
            item.range += 1

        # eat
        elif option.name == "eat":
            print "Nom Nom Nom"

        # touch
        elif option.name == "touch":
            print "Can't touch this"

        # Close menu when sub-option selected
        item.set_in_menu(grid, False)

    # Close menu if option has no sub-options
    if option.name not in grid.mode_vs_options.keys():
        item.set_in_menu(grid, False)