#######################################################################################################################
#################                                                                                     #################
#################                                 TimerItem class                                     #################
#################                                                                                     #################
#######################################################################################################################
import math
import time
from cir_item_mobile import MobileItem


class TimerItem(MobileItem):
    """ This is the base class for all timer items """
    def __init__(self, duration=0, time_color=None, tile_radius=None, start_time=None, **kwargs):
        super(TimerItem, self).__init__(**kwargs)

        self.start_time = start_time
        self.duration = duration
        self.time_color = time_color
        self.timer_tile_radius = tile_radius
        self._rect = []

        self.start_rad = 90
        self.filled_steps = self.start_rad
        self.step = 1

        self.time_step = 0.0157
        self._is_over = False
        self.number_of_steps = int(self.duration / self.time_step)
        self.len_step = -float(360) / self.number_of_steps

    def tick(self):
        """ Starts the timer, increasing the step and filled_steps """
        if not self.start_time:
            self.start_time = time.time()
        if self.start_time and not self.step == self.number_of_steps:
            if time.time() > (self.start_time + (self.time_step * self.step)):
                self.filled_steps += self.len_step
                self.step += 1

    @property
    def is_over(self):
        """ Returns a boolean if the timer is over """
        if self.start_time:
            if self.step == self.number_of_steps:
                self._is_over = True
        return self._is_over

    @property
    def rect(self):
        """ This defines the rect argument for the arch drawing """
        self._rect = [self.pos[0] - self.timer_tile_radius,
                self.pos[1] - self.timer_tile_radius,
                2 * self.timer_tile_radius,
                2 * self.timer_tile_radius]
        return self._rect


