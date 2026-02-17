import math


class Bug3:

    def __init__(self, grid, start, goal):

        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

        self.start = start
        self.goal = goal

        self.pos = start
        self.mode = "GOAL"

        self.hit_point = None
        self.hit_distance = None

        self.path = [self.pos]

        self.memory = []

    # -------------------------------------------------
    # Distance to goal (Euclidean)
    # -------------------------------------------------
    def distance_to_goal(self, pos):
        return math.sqrt((pos[0] - self.goal[0])**2 +
                         (pos[1] - self.goal[1])**2)

    # -------------------------------------------------
    def is_free(self, p):
        r, c = p
        if r < 0 or c < 0 or r >= self.rows or c >= self.cols:
            return False
        return self.grid[r][c] == 0

    # -------------------------------------------------
    # Simulated Range Sensor (Look ahead)
    # -------------------------------------------------
    def range_in_direction(self, direction, max_range=5):

        r, c = self.pos
        dr, dc = direction

        for i in range(1, max_range + 1):
            check = (r + dr * i, c + dc * i)
            if not self.is_free(check):
                return i - 1

        return max_range

    # -------------------------------------------------
    # Move directly toward goal
    # -------------------------------------------------
    def move_toward_goal(self):

        r, c = self.pos
        gr, gc = self.goal

        dr = 1 if gr > r else -1 if gr < r else 0
        dc = 1 if gc > c else -1 if gc < c else 0

        next_pos = (r + dr, c + dc)

        if self.is_free(next_pos):
            return next_pos
        else:
            self.mode = "BOUNDARY"
            self.hit_point = self.pos
            self.hit_distance = self.distance_to_goal(self.pos)
            return self.follow_boundary()

    # -------------------------------------------------
    # Right-hand rule boundary following
    # -------------------------------------------------
    def follow_boundary(self):

        r, c = self.pos

        directions = [
            (0, 1),   # Right
            (1, 0),   # Down
            (0, -1),  # Left
            (-1, 0)   # Up
        ]

        for d in directions:
            new_pos = (r + d[0], c + d[1])
            if self.is_free(new_pos) and new_pos not in self.memory:
                self.memory.append(self.pos)
                if len(self.memory) > 6:
                    self.memory.pop(0)
                return new_pos

        return self.pos

    # -------------------------------------------------
    # Step Function
    # -------------------------------------------------
    def step(self):

        if self.pos == self.goal:
            return self.pos, True

        if self.mode == "GOAL":

            # Check range in goal direction
            r, c = self.pos
            gr, gc = self.goal

            dr = 1 if gr > r else -1 if gr < r else 0
            dc = 1 if gc > c else -1 if gc < c else 0

            if self.range_in_direction((dr, dc)) > 0:
                self.pos = self.move_toward_goal()
            else:
                self.mode = "BOUNDARY"
                self.hit_point = self.pos
                self.hit_distance = self.distance_to_goal(self.pos)
                self.pos = self.follow_boundary()

        elif self.mode == "BOUNDARY":

            # Leave condition (Bug3 main idea)
            current_distance = self.distance_to_goal(self.pos)

            r, c = self.pos
            gr, gc = self.goal
            dr = 1 if gr > r else -1 if gr < r else 0
            dc = 1 if gc > c else -1 if gc < c else 0

            if (current_distance < self.hit_distance and
                self.range_in_direction((dr, dc)) > 0):

                self.mode = "GOAL"
                self.pos = self.move_toward_goal()

            else:
                self.pos = self.follow_boundary()

        self.path.append(self.pos)
        return self.pos, False
