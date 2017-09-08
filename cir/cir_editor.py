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

        # BUS
        if clicked_item.name == "EDITOR5":
            my_body.change_speed(0.5)

        # MAPS
        elif clicked_item.name == "EDITOR6":
            self.grid.event_effects.show_map(my_body)

        # CAMERA
        elif clicked_item.name == "EDITOR7":
            self.grid.capture_room()

        # TV
        elif clicked_item.name == "EDITOR8":
            my_body.range += 0.5

        if clicked_item.name == "EDITOR11":
            if my_body.lifespan:
                my_body.lifespan.update(10)

        elif clicked_item.name == "EDITOR12":
            if my_body.lifespan:
                my_body.lifespan.update(-10)

        elif clicked_item.name == "EDITOR13":
            my_body.img = self.grid.images.ape
            my_body.default_img = self.grid.images.ape
            my_body.speed = 10

        elif clicked_item.name == "EDITOR14":
            my_body.lifespan = None
            # my_body.lifespan.update(200)

        elif clicked_item.name == "EDITOR15" and not self.grid.current_room == "999":
            self.grid.event_effects.satellite()

        elif clicked_item.name == "EDITOR16":
            if my_body.lifespan:
                my_body.lifespan.duration = 60
                my_body.lifespan.restart()

        elif clicked_item.name == "EDITOR17":
            self.grid.scenario = 'scenario_2'
            self.grid.game_over = True

        # HOT-DOG
        elif clicked_item.name == "EDITOR18":
            my_body.vibe_speed += 0.1
            my_body.gen_fat()