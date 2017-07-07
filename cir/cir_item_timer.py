#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                                 TimerItem class                                     #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
import time
from cir_item_mobile import MobileItem


class TimerItem(MobileItem):
    """ This is the base class for all timer items """

    def __init__(self, duration=0, time_color=None, tile_radius=None, start_time=None, **kwargs):
        super(TimerItem, self).__init__(**kwargs)

        # VISUAL
        self.time_color = time_color
        self.timer_tile_radius = tile_radius
        self._rect = []

        # PARAMS
        self.duration = duration
        self.start_time = start_time

        # CONSTANTS
        self.step = 1
        self.start_rad = 90
        self.time_step = 0.0157

        # METRICS
        self.filled_steps = self.start_rad
        self._number_of_steps = int(self.duration / self.time_step)
        self._len_step = None
        self._is_over = False


    @property
    def number_of_steps(self):
        self._number_of_steps = int(self.duration / self.time_step)
        return self._number_of_steps

    @property
    def len_step(self):
        if self._number_of_steps > 0:
            self._len_step = -float(360) / self._number_of_steps
            return self._len_step

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
        if self.timer_tile_radius:
            self._rect = [self.pos[0] - self.timer_tile_radius,
                    self.pos[1] - self.timer_tile_radius,
                    2 * self.timer_tile_radius,
                    2 * self.timer_tile_radius]
        return self._rect

    def tick(self):
        """ Starts the timer, increasing the step and filled_steps """
        if self.available:
            if not self.start_time:
                self.start_time = time.time()
            if self.start_time and not self.step == self.number_of_steps:
                if time.time() > (self.start_time + (self.time_step * self.step)):
                    self.filled_steps += self.len_step
                    self.step += 1
