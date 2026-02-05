import math

# 4-connected grid (clockwise order)
DIRS = [
    (0, 1),   # right
    (1, 0),   # down
    (0, -1),  # left
    (-1, 0),  # up
]


class Bug2:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

        self.start = start
        self.goal = goal

        self.pos = start
        self.path = [start]

        self.mode = "GOAL"
        self.hit_point = None

        self.heading = 0  # direction index

    # ---------- helpers ----------

    def is_free(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] == 0

    def dist(self, p):
        return math.hypot(self.goal[0] - p[0], self.goal[1] - p[1])

    def on_mline(self, p):
        (x1, y1) = self.start
        (x2, y2) = self.goal
        (x, y) = p
        return abs((y2 - y1)*(x - x1) - (x2 - x1)*(y - y1)) < 0.5

    # ---------- goal seeking ----------

    def step_goal(self):
        r, c = self.pos
        gr, gc = self.goal

        dr = 1 if gr > r else -1 if gr < r else 0
        dc = 1 if gc > c else -1 if gc < c else 0

        options = [(r+dr, c), (r, c+dc)]

        for i, (nr, nc) in enumerate(options):
            if self.is_free(nr, nc):
                self.heading = i
                return (nr, nc)

        return None

    # ---------- right-hand wall follow ----------

    def follow_boundary(self):
        r, c = self.pos

        # try turning right relative to heading
        for i in range(4):
            idx = (self.heading - i) % 4
            dr, dc = DIRS[idx]
            nr, nc = r + dr, c + dc

            if self.is_free(nr, nc):
                self.heading = idx
                return (nr, nc)

        return self.pos

    # ---------- main step ----------

    def step(self):
        if self.pos == self.goal:
            return self.pos, True

        if self.mode == "GOAL":
            nxt = self.step_goal()

            if nxt is None:
                self.mode = "BOUNDARY"
                self.hit_point = self.pos
                nxt = self.follow_boundary()

        else:  # boundary mode
            nxt = self.follow_boundary()

            if self.on_mline(nxt) and self.dist(nxt) < self.dist(self.hit_point):
                self.mode = "GOAL"

        self.pos = nxt
        self.path.append(nxt)

        return nxt, False
