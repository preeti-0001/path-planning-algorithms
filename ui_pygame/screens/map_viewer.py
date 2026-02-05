import pygame
import json
import os
from algorithms.bug2 import Bug2

FREE_COLOR = (35, 35, 35)
OBS_COLOR = (180, 60, 60)
GRID_LINE = (55, 55, 55)

START_COLOR = (60, 200, 60)
GOAL_COLOR = (60, 60, 200)

ROBOT_COLOR = (255, 255, 0)
PATH_COLOR = (255, 180, 0)
MLINE_COLOR = (0, 200, 255)
HIT_COLOR = (255, 0, 255)

BG = (15, 15, 15)

CELL = 30
MARGIN = 40
SIDE_PANEL = 220


class MapViewer:

    def __init__(self, screen, map_name):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 20)

        self.load_map(map_name)

        self.planner = None
        self.path = []
        self.robot = self.start

        # continuous position
        self.robot_pos = [self.start[0]+0.5, self.start[1]+0.5]
        self.target_pos = self.robot_pos[:]

        self.playing = False
        self.timer = 0
        self.step_delay = 60

        self.back_rect = pygame.Rect(10, 10, 100, 35)
        self.next_screen = None

    # ---------- load map ----------

    def load_map(self, name):
        path = os.path.join("maps", name)
        with open(path) as f:
            data = json.load(f)

        self.grid = data["grid"]
        self.start = tuple(data["start"])
        self.goal = tuple(data["goal"])
        self.rows = data["height"]
        self.cols = data["width"]

    # ---------- coordinate helpers ----------

    def cell_to_pixel(self, r, c):
        x = MARGIN + c * CELL
        y = MARGIN + r * CELL
        return x, y

    def plane_to_pixel(self, pr, pc):
        x = MARGIN + pc * CELL
        y = MARGIN + pr * CELL
        return int(x), int(y)

    # ---------- planner ----------

    def run_bug2(self):
        self.planner = Bug2(self.grid, self.start, self.goal)
        self.path = [self.start]
        self.robot = self.start

        self.robot_pos = [self.start[0]+0.5, self.start[1]+0.5]
        self.target_pos = self.robot_pos[:]

        self.playing = True
        self.timer = 0

    # ---------- events ----------

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.back_rect.collidepoint(event.pos):
                from ui_pygame.screens.home_screen import HomeScreen
                self.next_screen = HomeScreen(self.screen)

            self.handle_slider(event.pos)

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                self.run_bug2()

    # ---------- slider ----------

    def handle_slider(self, pos):
        if not self.path:
            return

        sx = self.screen.get_width() - SIDE_PANEL + 20
        sy = 400
        sw = 160

        x, y = pos
        if sx <= x <= sx + sw and sy <= y <= sy + 20:
            ratio = (x - sx) / sw
            idx = int(ratio * (len(self.path) - 1))
            self.robot = self.path[idx]
            self.robot_pos = [self.robot[0]+0.5, self.robot[1]+0.5]
            self.playing = False

    # ---------- update ----------

    def update(self, dt):

        if self.next_screen:
            self.__class__ = self.next_screen.__class__
            self.__dict__ = self.next_screen.__dict__
            return

        # planner stepping
        if self.playing and self.planner:

            self.timer += dt
            if self.timer >= self.step_delay:
                self.timer = 0

                pos, done = self.planner.step()
                self.robot = pos
                self.path.append(pos)

                self.target_pos = [pos[0]+0.5, pos[1]+0.5]

                if done:
                    self.playing = False

        # smooth interpolation
        speed = 0.15
        self.robot_pos[0] += (self.target_pos[0] - self.robot_pos[0]) * speed
        self.robot_pos[1] += (self.target_pos[1] - self.robot_pos[1]) * speed

    # ---------- draw m-line ----------

    def draw_mline(self):

        if not self.planner:
            return

        for p in self.planner.mline:
            x, y = self.plane_to_pixel(*p)
            pygame.draw.circle(self.screen, (0,200,255), (x,y), 2)

# ---------- draw world ----------

    def draw_grid(self):

        for r in range(self.rows):
            for c in range(self.cols):
                x, y = self.cell_to_pixel(r, c)
                rect = pygame.Rect(x, y, CELL, CELL)

                if self.grid[r][c] == 1:
                    pygame.draw.rect(self.screen, OBS_COLOR, rect)
                else:
                    pygame.draw.rect(self.screen, FREE_COLOR, rect)

                pygame.draw.rect(self.screen, GRID_LINE, rect, 1)

        # path
        for p in self.path:
            x, y = self.cell_to_pixel(*p)
            pygame.draw.circle(self.screen, PATH_COLOR, (x+CELL//2, y+CELL//2), 4)

        # robot (continuous)
        rx, ry = self.plane_to_pixel(*self.robot_pos)
        
        pygame.draw.circle(self.screen, ROBOT_COLOR, (rx, ry), 10)
        # start & goal markers
        sx, sy = self.cell_to_pixel(*self.start)
        gx, gy = self.cell_to_pixel(*self.goal)

        pygame.draw.circle(self.screen, START_COLOR, (sx+CELL//2, sy+CELL//2), 10)
        pygame.draw.circle(self.screen, GOAL_COLOR, (gx+CELL//2, gy+CELL//2), 10)


    # ---------- back button ----------

    def draw_back_button(self):
        mouse = pygame.mouse.get_pos()
        color = (80,80,80) if self.back_rect.collidepoint(mouse) else (60,60,60)

        pygame.draw.rect(self.screen, color, self.back_rect, border_radius=6)

        label = self.font.render("Back", True, (255,255,255))
        rect = label.get_rect(center=self.back_rect.center)
        self.screen.blit(label, rect)

    # ---------- panel ----------

    def draw_panel(self):
        w = self.screen.get_width()
        panel = pygame.Rect(w - SIDE_PANEL, 0, SIDE_PANEL, self.screen.get_height())
        pygame.draw.rect(self.screen, (40, 40, 40), panel)

        title = self.font.render("Algorithm: Bug2", True, (255,255,255))
        self.screen.blit(title, (w - SIDE_PANEL + 20, 30))

    # ---------- draw ----------

    def draw(self):
        self.screen.fill(BG)
        self.draw_grid()
        self.draw_panel()
        self.draw_back_button()
        self.draw_mline()
