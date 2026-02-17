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

        # Boundary variables
        self.hit_point = None
        self.hit_distance = None
        self.best_leave_point = None
        self.best_distance = float("inf")
        self.boundary_start = None
        self.boundary_visited = set()

        # Right-hand rule directions (clockwise)
        self.directions = [
            (0, 1),    # Right
            (1, 0),    # Down
            (0, -1),   # Left
            (-1, 0)    # Up
        ]
        self.current_dir_index = 0

        self.path = [self.pos]

    # -------------------------------------------------
    # Utilities
    # -------------------------------------------------
    def is_free(self, p):
        r, c = p
        if r < 0 or c < 0 or r >= self.rows or c >= self.cols:
            return False
        return self.grid[r][c] == 0

    def distance_to_goal(self, pos):
        return math.hypot(pos[0] - self.goal[0],
                          pos[1] - self.goal[1])

    # -------------------------------------------------
    # Line-of-sight using Bresenham
    # -------------------------------------------------
    def line_of_sight_clear(self, p):

        x1, y1 = p
        x2, y2 = self.goal

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            if not self.is_free((x1, y1)):
                return False

            if (x1, y1) == (x2, y2):
                break

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

        return True

    # -------------------------------------------------
    # Move toward goal greedily
    # -------------------------------------------------
    def move_toward_goal(self):

        r, c = self.pos
        gr, gc = self.goal

        dr = 1 if gr > r else -1 if gr < r else 0
        dc = 1 if gc > c else -1 if gc < c else 0

        next_pos = (r + dr, c + dc)

        if self.is_free(next_pos):
            return next_pos

        # Hit obstacle
        self.mode = "BOUNDARY"
        self.hit_point = self.pos
        self.boundary_start = self.pos
        self.hit_distance = self.distance_to_goal(self.pos)
        self.best_leave_point = None
        self.best_distance = float("inf")
        self.boundary_visited = set()

        return self.follow_boundary()

    # -------------------------------------------------
    # True Right-Hand Rule Boundary Following
    # -------------------------------------------------
    def follow_boundary(self):

        r, c = self.pos

        for i in range(4):
            idx = (self.current_dir_index + i) % 4
            dr, dc = self.directions[idx]
            next_pos = (r + dr, c + dc)

            if self.is_free(next_pos):
                self.current_dir_index = idx
                return next_pos

        return self.pos

    # -------------------------------------------------
    # Step
    # -------------------------------------------------
    def step(self):

        if self.pos == self.goal:
            return self.pos, True

        # ---------------- GOAL MODE ----------------
        if self.mode == "GOAL":

            self.pos = self.move_toward_goal()

        # -------------- BOUNDARY MODE --------------
        elif self.mode == "BOUNDARY":

            current_distance = self.distance_to_goal(self.pos)

            # Check leave condition candidate
            if (self.line_of_sight_clear(self.pos) and
                current_distance < self.hit_distance):

                if current_distance < self.best_distance:
                    self.best_distance = current_distance
                    self.best_leave_point = self.pos

            # Move along boundary
            next_pos = self.follow_boundary()

            # If full loop completed
            if next_pos == self.boundary_start:

                if self.best_leave_point is not None:
                    self.pos = self.best_leave_point
                    self.mode = "GOAL"
                    self.path.append(self.pos)
                    return self.pos, False
                else:
                    # No valid leave point → unreachable
                    return self.pos, True

            self.pos = next_pos

        self.path.append(self.pos)
        return self.pos, False
