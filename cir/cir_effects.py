#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                                        Effects                                      #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################

import copy


def produce(grid, product, position):
    """
    Produces an item from the everything dict
    :param grid: grid instance
    :param product: name of the item from the everything dict
    :param position: new position
    :return: the new item
    """
    new_item = None
    if position not in grid.occupado_tiles and position in grid.revealed_tiles:
        for name, item in grid.everything.items():
            if name == product:
                new_item = copy.deepcopy(item)
                new_item.img = item.img
                new_item.default_img = item.default_img
                new_item.pos = position
                new_item.available = True
                grid.items.append(new_item)
    return new_item

# --------------------------------------------------------------- #
#                         MOUSE MODES                             #
# --------------------------------------------------------------- #
def laino_mode_click(grid, clicked_circle):
    """
    For mode 'laino', if clicked produces an item
    :param grid: grid instance
    :param clicked_circle: the clicked circle
    """
    produce(grid, "shit", clicked_circle)


def shit_mode_click(grid, clicked_circle):
    """
    For mode 'shit', if clicked produces an item and exhausts mode uses
    :param grid: grid instance
    :param clicked_circle: the clicked circle
    """
    if grid.mouse_mode == "shit":
        for bag_item in grid.mode_vs_options["bag"]:
            if bag_item.name == grid.mouse_mode:
                if bag_item.uses:
                    produce(grid, "shit", clicked_circle)
                    bag_item.uses -= 1

# --------------------------------------------------------------- #
#                           BAG EFFECTS                           #
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
                new_item.color = option.color
                grid.mode_vs_options["bag"].append(new_item)
                item.available = False
                grid.items.remove(item)
                break

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
            break
