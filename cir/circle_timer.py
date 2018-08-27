# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                    TIMER                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import time
from circle import Circle


class Timer(Circle):
    """ This is the base class for all timers """

    def __init__(self):
        super(Timer, self).__init__()

        # CONSTANTS
        # self.time_step = 0.0157
        # self.time_step = 63
        self.time_step = 1
        self.start_degrees = 90

        # METRICS
        self.duration = 0
        self.limit = self.duration
        self.step = 1
        self.start_time = None
        self._number_of_steps = 1
        self._step_degrees = None
        self._filled_degrees = self.start_degrees
        self._is_over = False
        self.reversed = True
        self.available = True

    @property
    def number_of_steps(self):
        self._number_of_steps = self.duration * self.time_step
        return self._number_of_steps

    @property
    def step_degrees(self):
        if self._number_of_steps > 0:
            self._step_degrees = -float(360) / self._number_of_steps
            return self._step_degrees

    @property
    def filled_degrees(self):
        if not self.reversed:
            self._filled_degrees = self.start_degrees + (self.step_degrees * self.step)
            return self._filled_degrees
        else:
            self._filled_degrees = self.start_degrees + (self.step_degrees * (self.number_of_steps - self.step))
            return self._filled_degrees

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
        current_duration = self.duration - (self.step / self.time_step)
        steps_before = self.number_of_steps

        if current_duration + delta > self.limit:
            self.duration = self.limit
            self.restart()
        elif current_duration + delta <= 0:
            self._is_over = True
        else:
            steps_delta  = delta * self.time_step
            self.duration += delta
            self._filled_degrees = int((self.step * self.number_of_steps) / steps_before) - \
                                  (self.step_degrees * steps_delta)
