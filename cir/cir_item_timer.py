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

    def __init__(self, duration=0, time_color=None, tile_radius=None, **kwargs):
        super(TimerItem, self).__init__(**kwargs)

        # VISUAL
        self.time_color = time_color
        self.timer_tile_radius = tile_radius
        self._rect = []

        # CONSTANTS
        self.time_step = 0.0157
        self.steps_per_sec = 63
        self.start_degrees = 90

        # METRICS
        self.duration = duration
        self.filled_degrees = self.start_degrees
        self.step = 1
        self.start_time = None
        self._step_degrees = None
        self._number_of_steps = None
        self._is_over = False

    @property
    def number_of_steps(self):
        # self._number_of_steps = int(self.duration / self.time_step)
        self._number_of_steps = self.duration * self.steps_per_sec
        return self._number_of_steps

    @property
    def step_degrees(self):
        if self._number_of_steps > 0:
            self._step_degrees = -float(360) / self._number_of_steps
            return self._step_degrees

    @property
    def is_over(self):
        """ Returns a boolean if the timer is over """
        if self.start_time:
            if self.step > self.number_of_steps:
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

    def restart(self):
        """ Restarts the timer """
        self._is_over = False
        self.step = 1
        self.filled_degrees = self.start_degrees
        self.start_time = None

    def tick(self):
        """ Starts the timer, increasing the step and filled_degrees """
        if self.available:
            if not self.start_time:
                self.start_time = time.time()
            if not self.is_over:
                if time.time() > (self.start_time + (self.time_step * self.step)):
                    # self.filled_degrees = self.start_degrees + (self.step_degrees * self.step)
                    self.filled_degrees += self.step_degrees
                    self.step += 1


    def update(self, delta):
        """
        Updates the timer with delta seconds
        :param delta: change of timer in seconds
        """
        print "OLD DEGREES", self.filled_degrees
        old_number_of_steps = self.number_of_steps


        delta_degrees = None
        delta_steps = delta * self.steps_per_sec
        # if delta_steps:
        #     delta_degrees = -float(360) / delta_steps
        # print delta_degrees

        self.duration += delta
        self.step = int((self.step * self.number_of_steps) / old_number_of_steps)
        # self.filled_degrees += self.start_degrees + (self.step_degrees * delta_steps)
        # self.filled_degrees = self.start_degrees + (self.step_degrees * self.step)
        # self.filled_degrees += 20
        print "NEW DEGREES", self.filled_degrees

