class Lineup:

    def __init__(self, captain, util1, util2, util3, util4, util5):

        self.captain = captain
        self.util1 = util1
        self.util2 = util2
        self.util3 = util3
        self.util4 = util4
        self.util5 = util5

    def __lt__(self, other):
        return (self.projection > other.projection)

    def set_total_cost(self):
        self.cost = (self.captain.salary * 1.5) + self.util1.salary + \
            self.util2.salary + self.util3.salary + self.util4.salary + self.util5.salary

    def set_projection(self):

        self.projection = (self.captain.expected_fantasy_points * 1.5) + self.util1.expected_fantasy_points + \
            self.util2.expected_fantasy_points + \
            self.util3.expected_fantasy_points + \
            self.util4.expected_fantasy_points + self.util5.expected_fantasy_points
