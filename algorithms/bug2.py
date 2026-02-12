import math


class Bug2:

    def __init__(self, grid, start, goal):

        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

        self.start = start
        self.goal = goal

        self.pos = start
        self.path = [self.pos]

        self.mode = "GOAL"
        self.hit_point = None

        # Step 1: Make m-line
        self.mline = self.make_mline(start, goal)

        self.path = [self.pos]


    # -------------------------------------------------
    # Step 1: Create m-line using Bresenham
    # -------------------------------------------------
    def make_mline(self, start, goal):

        mline = []

        x1, y1 = start
        x2, y2 = goal

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1

        err = dx - dy

        while True:
            mline.append((x1, y1))
            if (x1, y1) == (x2, y2):
                break

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

        return mline


    # -------------------------------------------------
    def is_free(self, p):
        r, c = p
        if r < 0 or c < 0 or r >= self.rows or c >= self.cols:
            return False
        return self.grid[r][c] == 0

    # -------------------------------------------------
    # Step 2: Follow m-line
    # -------------------------------------------------
    def follow_mline(self):

        idx = self.mline.index(self.pos)

        if idx + 1 >= len(self.mline):
            return self.pos

        next_cell = self.mline[idx + 1]

        if self.is_free(next_cell):
            return next_cell
        else:
            # Step 3: Hit obstacle
            self.mode = "BOUNDARY"
            self.hit_point = self.pos
            return self.move_around_obstacle()

    
    # ------------------------------------------------- 
    # Step 3: Proper Boundary Following (Right-Hand Rule) 
    # ------------------------------------------------- 
    def has_obstacle_neighbor(self, pos): 
        r, c = pos 
     
        neighbors = [ 
            (r+1, c), 
            (r-1, c), 
            (r, c+1), 
            (r, c-1),
            (r+1, c+1), 
            (r-1, c-1), 
            (r+1, c-1), 
            (r-1, c+1) 
        ] 
     
        for n in neighbors: 
            if not self.is_free(n): 
                return True 
     
        return False 
    
    def has_moved_here(self, pos): 
        for n in self.path:
            if n == pos:
                return True 
     
        return False 
    
    def move_around_obstacle(self): 
     
        r, c = self.pos 
     
        neighbors = [ 
            (r+1, c), 
            (r-1, c), 
            (r, c+1), 
            (r, c-1) 
        ] 
     
     
        for d in neighbors: 
            new_pos = (d[0], d[1]) 
            if self.is_free(new_pos) and self.has_obstacle_neighbor(new_pos) and not self.has_moved_here(new_pos): 
                self.dir = d 
                self.path.append(new_pos)
                return new_pos
            
        self.path.append(self.pos)
        return self.pos 
    
    

    # -------------------------------------------------
    # Step 4 & 5
    # -------------------------------------------------
    def step(self):

        if self.pos == self.goal:
            return self.pos, True

        if self.mode == "GOAL":
            self.pos = self.follow_mline()

        elif self.mode == "BOUNDARY":
            self.pos = self.move_around_obstacle()

            if self.pos in self.mline:
                if self.mline.index(self.pos) > self.mline.index(self.hit_point):
                    self.mode = "GOAL"

        self.path.append(self.pos)
        return self.pos, False

