import pygame
import json
import os

MAP_FOLDER = "maps"

GRID_SIZE = 20
CELL_SIZE = 30
MARGIN = 10

COLOR_BG = (25, 25, 25)
COLOR_GRID = (60, 60, 60)
COLOR_OBS = (200, 60, 60)
COLOR_START = (60, 200, 60)
COLOR_GOAL = (60, 60, 200)
COLOR_BTN = (70, 70, 70)
COLOR_BTN_HOVER = (100, 100, 100)


class MapEditor:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 22)

        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.start = (0, 0)
        self.goal = (GRID_SIZE - 1, GRID_SIZE - 1)

        self.message = ""

        # Back button
        self.back_rect = pygame.Rect(820, 10, 150, 40)

    # ---------------- GRID UTILS ----------------

    def grid_to_pixel(self, r, c):
        x = MARGIN + c * CELL_SIZE
        y = MARGIN + r * CELL_SIZE + 60  # push grid down
        return x, y

    def pixel_to_grid(self, x, y):
        y -= 60
        c = (x - MARGIN) // CELL_SIZE
        r = (y - MARGIN) // CELL_SIZE
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            return r, c
        return None

    def toggle_cell(self, r, c):
        if (r, c) != self.start and (r, c) != self.goal:
            self.grid[r][c] = 1 - self.grid[r][c]

    # ---------------- SAVE ----------------

    def save_map(self):
        if not os.path.exists(MAP_FOLDER):
            os.makedirs(MAP_FOLDER)

        name = f"user_map_{len(os.listdir(MAP_FOLDER))}.json"

        data = {
            "name": name,
            "width": GRID_SIZE,
            "height": GRID_SIZE,
            "grid": self.grid,
            "start": list(self.start),
            "goal": list(self.goal),
        }

        path = os.path.join(MAP_FOLDER, name)

        with open(path, "w") as f:
            json.dump(data, f, indent=2)

        self.message = f"Saved {name}"

    # ---------------- EVENTS ----------------

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_rect.collidepoint(event.pos):
                from ui_pygame.screens.home_screen import HomeScreen
                return HomeScreen(self.screen)

            cell = self.pixel_to_grid(*event.pos)
            if cell:
                self.toggle_cell(*cell)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from ui_pygame.screens.home_screen import HomeScreen
                return HomeScreen(self.screen)

            mouse = pygame.mouse.get_pos()
            cell = self.pixel_to_grid(*mouse)

            if cell:
                if event.key == pygame.K_s:
                    self.start = cell
                if event.key == pygame.K_g:
                    self.goal = cell

            if event.key == pygame.K_RETURN:
                self.save_map()

        return None

    # ---------------- LOOP ----------------

    def update(self, dt):
        pass

    # ---------------- DRAW ----------------

    def draw_grid(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x, y = self.grid_to_pixel(r, c)
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

                color = COLOR_GRID
                if self.grid[r][c] == 1:
                    color = COLOR_OBS
                if (r, c) == self.start:
                    color = COLOR_START
                if (r, c) == self.goal:
                    color = COLOR_GOAL

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

    def draw_ui(self):
        instructions = [
            "Click: toggle obstacle",
            "S: set start",
            "G: set goal",
            "ENTER: save map",
            "ESC: back",
        ]

        y = 10
        panel_x = self.screen.get_width() - 260 
        for text in instructions:
            label = self.font.render(text, True, (220, 220, 220))
            self.screen.blit(label, (panel_x, y))
            y += 25

        # message
        msg = self.font.render(self.message, True, (255, 200, 100))
        self.screen.blit(msg, (panel_x, y + 10))


    def draw(self):
        self.screen.fill(COLOR_BG)
        self.draw_grid()
        self.draw_ui()
