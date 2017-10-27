# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                                                                                     #
#                                                    EDITOR                                                           #
#                                                                                                                     #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
class Editor(object):

    def __init__(self, grid=None):
        self.grid = grid


    def execute_editor_clicks(self, clicked_item, my_body):
        """ EDITOR CLICKS """

        # PHONE
        if clicked_item.name == "EDITOR4":
            self.grid.show_debug = not self.grid.show_debug
            self.grid.show_grid = not self.grid.show_grid

        # BUS
        elif clicked_item.name == "EDITOR5":
            my_body.change_speed(0.5)

        # MAPS
        elif clicked_item.name == "EDITOR6":
            self.grid.event_effects.show_map(my_body)

        # CAMERA
        elif clicked_item.name == "EDITOR7":
            pass

        # TV
        elif clicked_item.name == "EDITOR8":
            my_body.range += 0.5

        # PIZZA
        if clicked_item.name == "EDITOR11":
            if my_body.lifespan:
                my_body.lifespan.update(30)

        # CIGARETTE
        elif clicked_item.name == "EDITOR12":
            if my_body.lifespan:
                my_body.lifespan.update(-10)

        # APE
        elif clicked_item.name == "EDITOR13":
            my_body.img = self.grid.images.ape
            my_body.default_img = self.grid.images.ape
            my_body.speed = 10

        # SPRITZ
        elif clicked_item.name == "EDITOR14":
            my_body.lifespan = None
            # my_body.lifespan.update(200)

        elif clicked_item.name == "EDITOR15" and not self.grid.current_room == "999":
            self.grid.event_effects.satellite()

        # PILL
        elif clicked_item.name == "EDITOR16":
            if my_body.lifespan:
                my_body.lifespan.duration = 60
                my_body.lifespan.restart()

        # SHROOM
        elif clicked_item.name == "EDITOR17":
            self.grid.scenario = 'scenario_02'
            self.grid.game_over = True

        # HOT-DOG
        elif clicked_item.name == "EDITOR18":
            my_body.vspeed += 0.1
            my_body.gen_fat()

        # FEM SULEIMAN
        elif clicked_item.name == "EDITOR25":
            for rev_tile in self.grid.revealed_tiles.keys():
                if rev_tile not in self.grid.occupado_tiles.values():
                    self.grid.event_effects.produce("observer", rev_tile)

        # FULL MOON
        elif clicked_item.name == "EDITOR20":
            my_body.range += 3
            my_body.vspeed += 6
            my_body.gen_effect_track(self.grid.red01)

        # BARREL
        elif clicked_item.name == "EDITOR19":
            my_body.effects += " LP_-180"
            my_body.gen_effect_track(self.grid.black)