"""
================================== Body class ==================================
"""


from math import sqrt


class Body(object):
    def __init__(self):

        self.current_img = None
        self.color = None

        self.range = 1
        self.speed = 5
        self.muscle = 1
        self.mind = 0

        self.ego = 0
        self.charm = 1
        self.lux = 1

        self.vision = 1
        self.audio = 0
        self.smell = 0
        self.touch = 0
        self.eat = 0

        self.spirit = 100
        self.lifespan = 100
        self.hygiene = 100
        self.stress = 0

        self.status = []

        self.pos = ()
        self.move_track = []

    # @property
    # def _pos(self):
    #     self._pos = (self.lead_x, self.lead_y)

    def tracks(self, Point_B):
        """
        :param Point_B: coordinates of destination point B (x, y)
        :param SPEED: pixels moved for each step
        :return: a list of steps from point A to point B
        """
        self.move_track = []
        ax = self.pos[0]
        ay = self.pos[1]
        bx = Point_B[0]
        by = Point_B[1]
        dx, dy = (bx - ax, by - ay)
        distance = sqrt(dx ** 2 + dy ** 2)
        steps_number = int(distance / self.speed)
        if steps_number > 0:
            stepx, stepy = int(dx / steps_number), int(dy / steps_number)
            for i in range(steps_number + 1):
                step = (int(ax + stepx * i), int(ay + stepy * i))
                self.move_track.append(step)
        self.move_track.append(Point_B)
        return self.move_track

    def move(self):
        if self.move_track:
            self.pos = self.move_track[0]
            self.move_track.pop(0)