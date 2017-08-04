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
import time

# --------------------------------------------------------------- #
#                                                                 #
#                         BASIC EFFECTS                           #
#                                                                 #
# --------------------------------------------------------------- #
def produce(grid, product_name, pos, loader, radius=None, birth=None,):
    """
    Produces an item from the everything dict
    :param grid: grid instance
    :param product: name of the item from the everything dict
    :param pos: new position
    :return: the new item
    """

    new_item = loader.load_item(product_name)

    if radius:
        new_item.radius = radius
    if birth:
        new_item.birth_time.duration = birth
    new_item.pos = pos
    new_item.default_img = new_item.img
    new_item.name = new_item.name + str(time.time())
    new_item.available = True
    new_item.gen_birth_track()

    grid.items.append(new_item)
    return new_item

    # new_item = None
    # for name, item in grid.everything.items():
    #     if name == product_name:
    #         new_item = copy.deepcopy(item)
    #         if radius:
    #             new_item.radius = radius
    #         if birth:
    #             new_item.birth_time.duration = birth
    #         new_item.name = new_item.name + str(time.time())
    #         new_item.img = item.img
    #         new_item.default_img = item.default_img
    #         new_item.pos = pos
    #         new_item.available = True
    #         new_item.gen_birth_track()
    #         new_item.lifespan = item.lifespan
    #         new_item.marked_for_destruction = False
    #         grid.items.append(new_item)


def destroy(grid, item):
    if item in grid.items and not item.birth_track:
        item.in_menu = False
        if item.lifespan:
            item.lifespan = None
        item.move_track = []
        item.gen_birth_track()
        item.birth_track.reverse()

        item.marked_for_destruction = True


def destruction(grid, item):
    if item.marked_for_destruction and not item.birth_track:
        item.available = False
        grid.items.remove(item)
        if item.name == "my_body":
            grid.game_over = True


# --------------------------------------------------------------- #
#                                                                 #
#                         MOUSE MODES                             #
#                                                                 #
# --------------------------------------------------------------- #
def laino_mode_click(grid, current_tile, loader):
    """
    For mode 'laino', if clicked produces an item
    :param grid: grid instance
    :param current_tile: the clicked circle
    """
    if current_tile not in grid.occupado_tiles and current_tile in grid.revealed_tiles:
        produce(grid, "product_shit", current_tile, loader)


def shit_mode_click(grid, current_circle, loader):
    """
    For mode 'shit', if clicked produces an item and exhausts mode uses
    :param grid: grid instance
    :param current_circle: the clicked circle
    """
    for bag_item in grid.mode_vs_options["bag"]:
        if bag_item.name == grid.mouse_mode:
            if bag_item.uses:
                if current_circle not in grid.occupado_tiles: #and current_circle in grid.revealed_tiles:
                    produce(grid, "shit", current_circle, loader)
                    bag_item.uses -= 1
                    return 1


def eat_mode_click(grid, current_tile):
    """ Eat that shit """
    for item in grid.items:
        if current_tile == item.pos and not item.name == "my_body" and not "EDITOR" in item.name:
            destroy(grid, item)


def echo_mode_click(grid, current_tile, my_body, MOUSE_POS, loader):
    """ Signal effect """
    if not cir_utils.in_circle(my_body.pos, my_body.radius, current_tile) and not my_body.move_track:
        signal = produce(grid,
                         "signal",
                         my_body.pos,
                         radius = int(grid.tile_radius / 3),
                         birth = 0,
                         loader = loader)
        signal.direction = signal.get_aiming_direction(grid, current_tile, MOUSE_POS)[1]


def signal_hit(gird, item, my_body):
    hit = False
    if item.type == "signal":
        if (item.pos in gird.occupado_tiles and not item.intersects(my_body)) or item.direction == None:
            hit = True
            print "Hit!"
    return hit


def signal_hit_effect(grid, item):
    item.in_menu = False
    item.move_track = []
    item.gen_birth_track()
    item.birth_track.reverse()
    item.marked_for_destruction = True


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
            if item.lifespan:
                item.lifespan.restart()


def signal_lifespan_over_effect(grid, item):
    destroy(grid, item)


def timer_effect(grid, item):
    """ Timer effects  """
    if item.lifespan:
        item.lifespan.tick()

        if item.lifespan.is_over:
            if item.name == "my_body":
                my_body_lifespan_over_effect(grid)
            elif "observer" in item.name:
                observer_lifespan_over_effect(grid, item)
            else:
                destroy(grid, item)

    if item.birth_track:
        if item.birth_time and not isinstance(item.birth_time, float):
            item.birth_time.tick()
            if item.birth_time.is_over:
                birth_time_over_effect(item)


# --------------------------------------------------------------- #
#                        MOUSE MODE CLICK                         #
# --------------------------------------------------------------- #
def mouse_mode_click(grid, current_tile, my_body, MOUSE_POS, loader):
    if grid.mouse_mode in ["laino", "EDITOR2"]:
        laino_mode_click(grid, current_tile, loader)
    elif grid.mouse_mode in ["shit"]:
        shit_mode_click(grid, current_tile, loader)
    elif grid.mouse_mode in ["see", "EDITOR1"]:
        if current_tile not in grid.occupado_tiles and current_tile in grid.revealed_tiles:
            new_observer = produce(grid, "observer", current_tile, loader)
            new_observer.lifespan.restart()
    elif grid.mouse_mode in ["EDITOR3"]:
        if current_tile not in grid.occupado_tiles and current_tile in grid.revealed_tiles:
            produce(grid, "block_of_steel", current_tile, loader)
    elif grid.mouse_mode in ["eat", "EDITOR7"]:
        eat_mode_click(grid, current_tile)
    elif grid.mouse_mode == "echo":
        echo_mode_click(grid, current_tile, my_body, MOUSE_POS, loader)

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

        elif option.name == "suicide":
            destroy(grid, item)

        elif option.name == "echo":
            print "Echo!"

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