from os import stat
import numpy
import matplotlib.pyplot as plt
from scipy.stats import norm


class Player:

    def __init__(self, full_name, position, salary, id, dk_id):

        self.name = full_name
        self.position = position
        self.salary = salary
        self.api_id = id
        self.dk_id = dk_id
        self.injury_status = False
        self.ineligible = False

    def set_ineligible_status(self, status):
        self.ineligible = status

    def set_injury_status(self, status):
        self.injury_status = status

    def set_expected_threes(self, threes):
        self.expected_3pm = threes

    def set_average_threes(self, threes):
        self.average_3pm = threes

    def set_std_deviation_threes(self, threes):
        self.std_dev_3pm = threes

    def set_expected_pts(self, pts):
        self.expected_pts = pts

    def set_average_pts(self, pts):
        self.average_pts = pts

    def set_std_deviation_pts(self, pts):
        self.std_dev_pts = pts

    def set_expected_rebounds(self, rebounds):
        self.expected_rebounds = rebounds

    def set_average_rebounds(self, rebounds):
        self.average_rebounds = rebounds

    def set_std_deviation_rebounds(self, rebounds):
        self.std_dev_rebounds = rebounds

    def set_expected_assists(self, assists):
        self.expected_assists = assists

    def set_average_assists(self, assists):
        self.average_assists = assists

    def set_std_deviation_assists(self, assists):
        self.std_dev_assists = assists

    def set_expected_steals(self, steals):
        self.expected_steals = steals

    def set_average_steals(self, steals):
        self.average_steals = steals

    def set_std_deviation_steals(self, steals):
        self.std_dev_steals = steals

    def set_expected_blocks(self, blocks):
        self.expected_blocks = blocks

    def set_average_blocks(self, blocks):
        self.average_blocks = blocks

    def set_std_deviation_blocks(self, blocks):
        self.std_dev_blocks = blocks

    def set_expected_turnovers(self, turnovers):
        self.expected_turnovers = turnovers

    def set_average_turnovers(self, turnovers):
        self.average_turnovers = turnovers

    def set_std_deviation_turnovers(self, turnovers):
        self.std_dev_turnovers = turnovers

    def set_expected_minutes(self, mins):
        self.expected_minutes = mins

    def set_expected_prj_min(self, prj_min):
        self.expected_prj_min = prj_min

    def set_doubles(self):

        doubles = 0

        if (self.expected_pts >= 10):
            doubles += 1

        if (self.expected_rebounds >= 10):
            doubles += 1

        if (self.expected_assists >= 10):
            doubles += 1

        if (self.expected_steals >= 10):
            doubles += 1

        if (self.expected_blocks >= 10):
            doubles += 1

        if (doubles >= 3):
            self.triple_double = True
            self.double_double = True
        elif (doubles == 2):
            self.triple_double = False
            self.double_double = True
        else:
            self.triple_double = False
            self.double_double = False

    def set_expected_fantasy_points(self):

        total_points = 0

        total_points += 1 * self.expected_pts
        total_points += .5 * self.expected_3pm
        total_points += 1.25 * self.expected_rebounds
        total_points += 1.5 * self.expected_assists
        total_points += 2 * self.expected_steals
        total_points += 2 * self.expected_blocks
        total_points -= .5 * self.expected_turnovers

        if (self.double_double):
            total_points += 1.5

        if (self.triple_double):
            total_points += 3

        self.expected_fantasy_points = total_points

    def set_random_fantasy_points(self):

        #x_axis = numpy.arange(0, 50, 1)
        #plt.plot(x_axis, norm.pdf(x_axis, self.average_pts, self.std_dev_pts), label=self.name)
        #plt.legend()
        #plt.show()

        random_3pm = numpy.random.normal(loc=self.average_3pm, scale=self.std_dev_3pm)
        random_pts = numpy.random.normal(loc=self.average_pts, scale=self.std_dev_pts)
        random_rebounds = numpy.random.normal(loc=self.average_rebounds, scale=self.std_dev_rebounds)
        random_assists = numpy.random.normal(loc=self.average_assists, scale=self.std_dev_assists)
        random_steals = numpy.random.normal(loc=self.average_steals, scale=self.std_dev_steals)
        random_blocks = numpy.random.normal(loc=self.average_blocks, scale=self.std_dev_blocks)
        random_turnovers = numpy.random.normal(loc=self.average_turnovers, scale=self.std_dev_turnovers)

        if random_3pm < 0:
            random_3pm = 0

        if random_pts < 0:
            random_pts = 0

        if random_rebounds < 0:
            random_rebounds = 0

        if random_assists < 0:
            random_assists = 0

        if random_steals < 0:
            random_steals = 0

        if random_blocks < 0:
            random_blocks = 0

        if random_turnovers < 0:
            random_turnovers = 0

        total_points = 0
        total_points += 1 * random_pts
        total_points += .5 * random_3pm
        total_points += 1.25 * random_rebounds
        total_points += 1.5 * random_assists
        total_points += 2 * random_steals
        total_points += 2 * random_blocks
        total_points -= .5 * random_turnovers

        doubles = 0

        if (random_pts >= 10):
            doubles += 1

        if (random_rebounds >= 10):
            doubles += 1

        if (random_assists >= 10):
            doubles += 1

        if (random_steals >= 10):
            doubles += 1

        if (random_blocks >= 10):
            doubles += 1

        double_double = False
        triple_double = False

        if (doubles >= 3):
            triple_double = True
            double_double = True
        elif (doubles == 2):
            triple_double = False
            double_double = True
        else:
            triple_double = False
            double_double = False

        if (double_double):
            total_points += 1.5

        if (triple_double):
            total_points += 3

        self.random_fantasy_points = total_points
