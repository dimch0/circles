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

        if clicked_item.name == "edit_phone":
            self.grid.show_debug = not self.grid.show_debug
            self.grid.show_grid = not self.grid.show_grid

        elif clicked_item.name == "edit_fast":
            my_body.change_speed(0.5)
            my_body.gen_effect_track(self.grid.white)

        elif clicked_item.name == "edit_map":
            self.grid.event_effects.show_map(my_body)

        elif clicked_item.name == "edit_slow":
            my_body.change_speed(-0.5)
            my_body.gen_effect_track(self.grid.red01)

        elif clicked_item.name == "edit_heal":
            if my_body.lifespan:
                my_body.lifespan.update(30)
                my_body.gen_effect_track(self.grid.white)

        elif clicked_item.name == "edit_poison":
            if my_body.lifespan:
                my_body.lifespan.update(-10)
                my_body.gen_effect_track(self.grid.red01)

        elif clicked_item.name == "edit_inf":
            my_body.lifespan = None
            my_body.gen_effect_track(self.grid.white)

        elif clicked_item.name == "edit_sat" and not self.grid.current_room == "999":
            self.grid.event_effects.satellite()

        elif clicked_item.name == "edit_spiral":
            self.grid.scenario = 'scenario_02'
            self.grid.game_over = True

        elif clicked_item.name == "edit_pentagram":
            for rev_tile in self.grid.revealed_tiles.keys():
                if rev_tile not in self.grid.occupado_tiles.values():
                    self.grid.event_effects.produce("observer", rev_tile)

        elif clicked_item.name == "edit_fi":
            # my_body.range += 0.5
            # my_body.vspeed += 0.1
            my_body.gen_fat()
            my_body.range += 4
            my_body.vspeed += 6
            my_body.gen_effect_track(self.grid.white)

        elif clicked_item.name == "edit_nuke":
            my_body.effects += " LP_-180"
            my_body.gen_effect_track(self.grid.white)