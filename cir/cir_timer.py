#######################################################################################################################
#################                                                                                     #################
#################                                 TimerItem class                                      #################
#################                                                                                     #################
#######################################################################################################################
import math
import time
from cir_mobile import MobileItem


class TimerItem(MobileItem):
    """ This is the base class for all timer items """
    def __init__(self, duration, time_color, start_time=None, **kwargs):
        super(TimerItem, self).__init__(**kwargs)

        self.time_color = time_color
        self.start_time = start_time
        self.duration = duration
        self._rect = []
        self.filled_steps = 90
        self.start_point = math.radians(self.filled_steps)
        self._filled_angle = None

        self.time_step = 0.0157
        self._number_of_steps = int(self.duration / self.time_step)
        self.len_step = -float(360) / self.number_of_steps
        self.step = 1
        self._is_over = False

    @property
    def number_of_steps(self):
        self._number_of_steps = int(self.duration / self.time_step)
        return self._number_of_steps


    def tick(self):
        """ Starts the timer, increasing the step and filled_steps """
        if not self.start_time:
            self.start_time = time.time()
        if self.start_time and not self.step == self._number_of_steps:
            if time.time() > (self.start_time + (self.time_step * self.step)):
                self.filled_steps += self.len_step
                self.step += 1

    @property
    def is_over(self):
        """ Returns a boolean if the timer is over """
        if self.start_time:
            if self.step == self._number_of_steps:
                self._is_over = True
        return self._is_over

    @property
    def filled_angle(self):
        """
        This defines the first radian argument for the arc drawing of timer
        stop_radian is at math.radians(-270)
        """
        self._filled_angle = math.radians(self.filled_steps)
        return self._filled_angle

    @property
    def rect(self):
        """ This defines the rect argument for the arch drawing """
        self._rect = [self.pos[0] - self.grid.tile_radius,
                self.pos[1] - self.grid.tile_radius,
                2 * self.grid.tile_radius,
                2 * self.grid.tile_radius]
        return self._rect


