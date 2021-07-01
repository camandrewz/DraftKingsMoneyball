class Player:

    def __init__(self, full_name, position, salary, id):

        self.name = full_name
        self.position = position
        self.salary = salary
        self.api_id = id

    def set_expected_threes(self, threes):
        self.expected_3pm = threes

    def set_expected_pts(self, pts):
        self.expected_pts = pts

    def set_expected_rebounds(self, rebounds):
        self.expected_rebounds = rebounds

    def set_expected_assists(self, assists):
        self.expected_assists = assists

    def set_expected_steals(self, steals):
        self.expected_steals = steals

    def set_expected_blocks(self, blocks):
        self.expected_blocks = blocks

    def set_expected_turnovers(self, turnovers):
        self.expected_turnovers = turnovers

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

    def set_expected_minutes(self, mins):
        self.expected_minutes = mins
