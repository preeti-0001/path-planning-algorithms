import pygame
import json
import os
from algorithms.bug2 import Bug2

GRID_COLOR = (60, 60, 60)
OBS_COLOR = (200, 60, 60)
START_COLOR = (60, 200, 60)
GOAL_COLOR = (60, 60, 200)
ROBOT_COLOR = (255, 255, 0)
PATH_COLOR = (255, 180, 0)
MLINE_COLOR = (0, 200, 255)
HIT_COLOR = (255, 0, 255)
BG = (20, 20, 20)

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
        self.playing = False

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

    def pixel_to_cell(self, x, y):
        c = (x - MARGIN) // CELL
        r = (y - MARGIN) // CELL
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return r, c
        return None

    # ---------- planner ----------

    def run_bug2(self):
        self.planner = Bug2(self.grid, self.start, self.goal)
        self.path = [self.start]
        self.robot = self.start
        self.playing = True

    # ---------- events ----------

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.run_bug2()

            if event.key == pygame.K_g:
                mouse = pygame.mouse.get_pos()
                cell = self.pixel_to_cell(*mouse)
                if cell:
                    self.goal = cell
                    self.run_bug2()

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_slider(event.pos)

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
            self.playing = False

    # ---------- update ----------

    def update(self, dt):
        if self.playing and self.planner:
            pos, done = self.planner.step()
            self.robot = pos
            self.path.append(pos)

            if done:
                self.playing = False

    # ---------- draw m-line ----------

    def draw_mline(self):
        sr, sc = self.start
        gr, gc = self.goal

        x1, y1 = self.cell_to_pixel(sr, sc)
        x2, y2 = self.cell_to_pixel(gr, gc)

        pygame.draw.line(
            self.screen,
            MLINE_COLOR,
            (x1 + CELL//2, y1 + CELL//2),
            (x2 + CELL//2, y2 + CELL//2),
            3,
        )

    # ---------- draw grid ----------

    def draw_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                x, y = self.cell_to_pixel(r, c)
                rect = pygame.Rect(x, y, CELL, CELL)

                color = GRID_COLOR
                if self.grid[r][c] == 1:
                    color = OBS_COLOR
                if (r, c) == self.start:
                    color = START_COLOR
                if (r, c) == self.goal:
                    color = GOAL_COLOR

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

        # draw path trail
        for p in self.path:
            x, y = self.cell_to_pixel(*p)
            pygame.draw.circle(self.screen, PATH_COLOR, (x + CELL//2, y + CELL//2), 4)

        # draw robot
        rx, ry = self.cell_to_pixel(*self.robot)
        pygame.draw.circle(self.screen, ROBOT_COLOR, (rx + CELL//2, ry + CELL//2), 10)

        # draw hit point
        if self.planner and self.planner.hit_point:
            hr, hc = self.planner.hit_point
            x, y = self.cell_to_pixel(hr, hc)
            pygame.draw.circle(self.screen, HIT_COLOR, (x + CELL//2, y + CELL//2), 10)

    # ---------- panel ----------

    def draw_panel(self):
        w = self.screen.get_width()
        panel = pygame.Rect(w - SIDE_PANEL, 0, SIDE_PANEL, self.screen.get_height())
        pygame.draw.rect(self.screen, (40, 40, 40), panel)

        title = self.font.render("Algorithm: Bug2", True, (255, 255, 255))
        self.screen.blit(title, (w - SIDE_PANEL + 20, 30))

        mode = "IDLE"
        if self.planner:
            mode = self.planner.mode

        label = self.font.render(f"Mode: {mode}", True, (255,255,255))
        self.screen.blit(label, (w - SIDE_PANEL + 20, 80))

        help_text = [
            "SPACE: run",
            "G + click: new goal",
            "drag slider: replay",
        ]

        y = 130
        for t in help_text:
            label = self.font.render(t, True, (200, 200, 200))
            self.screen.blit(label, (w - SIDE_PANEL + 20, y))
            y += 30

        # slider
        sx = w - SIDE_PANEL + 20
        sy = 400
        sw = 160

        pygame.draw.rect(self.screen, (90, 90, 90), (sx, sy, sw, 20))

        if self.path:
            ratio = self.path.index(self.robot) / max(1, len(self.path)-1)
            knob = sx + int(ratio * sw)
            pygame.draw.circle(self.screen, (255, 200, 0), (knob, sy + 10), 8)

    # ---------- draw ----------

    def draw(self):
        self.screen.fill(BG)
        self.draw_mline()
        self.draw_grid()
        self.draw_panel()
