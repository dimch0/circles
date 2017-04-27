#######################################################################################################################
#################                                                                                     #################
#################                                 TimerItem class                                      #################
#################                                                                                     #################
#######################################################################################################################
import pdb
import math
import time
from cir_mobile import MobileItem


class TimerItem(MobileItem):
    """
    This is the base class for all timer items
    """

    def __init__(self, duration, time_color, start_time=None, **kwargs):
        super(TimerItem, self).__init__(**kwargs)

        self.time_color = time_color
        self.start_point = math.radians(90)
        self.start_time = start_time
        self.duration = duration
        self.initial_step = 0.022
        self.timer_step = self.initial_step
        self._increase_filled_angle = -round((360 / (self.duration / self.initial_step)), 1)
        self._rect = []
        self.timer_tick = 90
        self._filled_angle = None
        self._is_over = False

    @property
    def increase_filled_angle(self):
        self._increase_filled_angle = -round((360 / (self.duration / self.initial_step)), 1)
        return self._increase_filled_angle

    def start_timer(self):
        if not self.start_time:
            self.start_time = round(time.time(), 1)
        if self.start_time:
            if round(time.time(), 1) >= round((self.start_time + self.timer_step), 1):
                self.timer_step += self.initial_step
                self.timer_tick += self._increase_filled_angle

    @property
    def filled_angle(self):
        """ The radian for the arc drawing of timer """
        # start_radian = math.radians(90)
        # stop_radian = math.radians(-270)

        self._filled_angle = math.radians(self.timer_tick)
        return self._filled_angle

    @property
    def rect(self):
        self._rect = [self.pos[0] - self.grid.tile_radius,
                self.pos[1] - self.grid.tile_radius,
                2 * self.grid.tile_radius,
                2 * self.grid.tile_radius]
        return self._rect