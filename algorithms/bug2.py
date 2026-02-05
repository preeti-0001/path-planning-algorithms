import math


class Bug2:

    def __init__(self, grid, start, goal):

        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

        self.start = (start[0] + 0.5, start[1] + 0.5)
        self.goal = (goal[0] + 0.5, goal[1] + 0.5)

        self.pos = list(self.start)
        self.path = [tuple(self.pos)]

        self.mode = "GOAL"
        self.hit_point = None

        self.step_size = 0.08

        # m-line direction
        dx = self.goal[0] - self.start[0]
        dy = self.goal[1] - self.start[1]
        mag = math.hypot(dx, dy)
        self.mdir = (dx / mag, dy / mag)

        # 🔥 precompute m-line samples for visualization
        self.mline = []
        p = list(self.start)

        while math.hypot(p[0] - self.goal[0], p[1] - self.goal[1]) > 0.1:
            self.mline.append(tuple(p))
            p[0] += self.mdir[0] * 0.1
            p[1] += self.mdir[1] * 0.1

        self.mline.append(self.goal)
        self.wall_dir = None

    # ---------- collision ----------

    def is_free(self, p):
        r = int(p[0])
        c = int(p[1])

        if r < 0 or c < 0 or r >= self.rows or c >= self.cols:
            return False

        return self.grid[r][c] == 0

    # ---------- distance ----------

    def dist(self, p):
        return math.hypot(self.goal[0] - p[0], self.goal[1] - p[1])

    # ---------- m-line check ----------

    def on_mline(self, p):
        x1, y1 = self.start
        x2, y2 = self.goal
        x, y = p
        return abs((y2 - y1) * (x - x1) - (x2 - x1) * (y - y1)) < 0.2

    # ---------- goal motion ----------

    def step_goal(self):

        nxt = [
            self.pos[0] + self.mdir[0] * self.step_size,
            self.pos[1] + self.mdir[1] * self.step_size,
        ]

        if self.is_free(nxt):
            return nxt

        return None

    # ---------- boundary follow ----------

    def follow_wall(self):


        eps = 0.05
        gx = 0
        gy = 0

        # estimate obstacle normal
        for dx in [-eps, eps]:
            for dy in [-eps, eps]:
                test = (self.pos[0] + dx, self.pos[1] + dy)
                if not self.is_free(test):
                    gx += dx
                    gy += dy

        mag = math.hypot(gx, gy)

        if mag == 0:
            return self.pos

        nx = gx / mag
        ny = gy / mag

        # tangent candidates
        t1 = (-ny, nx)
        t2 = (ny, -nx)

        # lock direction if first time
        if self.wall_dir is None:
            self.wall_dir = t1

        # try preferred direction first
        tx, ty = self.wall_dir

        nxt = [self.pos[0] + tx * self.step_size, self.pos[1] + ty * self.step_size]

        if self.is_free(nxt):
            return nxt

        # fallback to opposite tangent
        tx, ty = (-tx, -ty)
        self.wall_dir = (tx, ty)

        nxt = [self.pos[0] + tx * self.step_size, self.pos[1] + ty * self.step_size]

        return nxt

    # ---------- main step ----------

    def step(self):

        if self.dist(self.pos) < 0.2:
            return tuple(self.pos), True

        if self.mode == "GOAL":

            nxt = self.step_goal()

            if nxt is None:
                self.mode = "BOUNDARY"
                self.hit_point = tuple(self.pos)
                nxt = self.follow_wall()

        else:

            nxt = self.follow_wall()

            if self.on_mline(nxt) and self.dist(nxt) < self.dist(self.hit_point):
                self.mode = "GOAL"

        self.pos = nxt
        self.path.append(tuple(self.pos))

        return tuple(self.pos), False
