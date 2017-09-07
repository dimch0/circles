# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                    TIMER                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import time
from cir_item import Item


class TimerItem(Item):
    """ This is the base class for all timer items """

    def __init__(self):
        super(TimerItem, self).__init__()

        # CONSTANTS
        self.time_step = 0.0157
        self.steps_per_sec = 63
        self.start_degrees = 90

        # METRICS
        self.duration = 0
        self.limit = 0
        self.step = 1
        self.start_time = None
        self._number_of_steps = 1
        self._step_degrees = None
        self._filled_degrees = self.start_degrees
        self._is_over = False
        self.reversed = False

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
    def filled_degrees(self):
        try:
            if not self.reversed:
                self._filled_degrees = self.start_degrees + (self.step_degrees * self.step)
                return self._filled_degrees
            else:
                self._filled_degrees = self.start_degrees + (self.step_degrees * (self.number_of_steps - self.step))
                return self._filled_degrees
        except Exception as e:
            print "ERROR filled_degrees", e

    @property
    def is_over(self):
        """ Returns a boolean if the timer is over """
        if self.start_time:
            if self.step > self.number_of_steps:
                self._is_over = True
        return self._is_over

    def restart(self):
        """ Restarts the timer """
        self._is_over = False
        self.step = 1
        self.start_time = None

    def tick(self):
        """ Starts the timer, increasing the step and filled_degrees """
        if self.available:
            if not self.start_time:
                self.start_time = time.time()
            if not self.is_over:
                if time.time() > (self.start_time + (self.time_step * self.step)):
                    self.step += 1

    def update(self, delta):
        """
        Updates the timer with delta seconds
        :param delta: change of timer in seconds
        """
        current_duration = self.duration - (self.step / self.steps_per_sec)
        steps_before = self.number_of_steps

        if current_duration + delta > self.limit:
            self.duration = self.limit
            self.restart()
        elif current_duration + delta <= 0:
            self._is_over = True
        else:
            steps_delta  = delta * self.steps_per_sec
            self.duration += delta
            self._filled_degrees = int((self.step * self.number_of_steps) / steps_before) - \
                                  (self.step_degrees * steps_delta)


        # print "dur: ", self.duration
        # print current_duration + delta
        # print self.limit
        # print "current    step :", self.step
        # print "number of steps :", self.number_of_steps
        # print "start   degrees :", self.start_degrees
        # print "filled  degrees :", self.filled_degrees
        # print "step    degrees :", self.step_degrees
        # print "-" * 35
