import pygame

SIDE_PANEL_WIDTH = 220
PANEL_BG = (40, 40, 40)

TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (70, 70, 70)
BUTTON_HOVER = (100, 100, 100)
BUTTON_ACTIVE = (0, 150, 200)


class SidePanel:

    def __init__(self, screen, algorithms):

        self.screen = screen
        self.font = pygame.font.SysFont("arial", 20)

        self.algorithms = algorithms  # ["Bug2", "Bug3"]
        self.selected_algorithm = algorithms[0]

        self.buttons = []

        self.create_buttons()

    # --------------------------------------------
    def create_buttons(self):

        screen_w = self.screen.get_width()

        y = 120
        for algo in self.algorithms:

            rect = pygame.Rect(
                screen_w - SIDE_PANEL_WIDTH + 20,
                y,
                SIDE_PANEL_WIDTH - 40,
                40
            )

            self.buttons.append((algo, rect))
            y += 60

    # --------------------------------------------
    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            for algo, rect in self.buttons:
                if rect.collidepoint(event.pos):
                    self.selected_algorithm = algo
                    return algo   # tell MapViewer which one was chosen

        return None

    # --------------------------------------------
    def draw(self, planner):

        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()

        panel_rect = pygame.Rect(
            screen_w - SIDE_PANEL_WIDTH,
            0,
            SIDE_PANEL_WIDTH,
            screen_h
        )

        pygame.draw.rect(self.screen, PANEL_BG, panel_rect)

        # Title
        title = self.font.render("Select Algorithm", True, TEXT_COLOR)
        self.screen.blit(title, (screen_w - SIDE_PANEL_WIDTH + 20, 40))

        mouse = pygame.mouse.get_pos()

        for algo, rect in self.buttons:

            # Button color logic
            if algo == self.selected_algorithm:
                color = BUTTON_ACTIVE
            elif rect.collidepoint(mouse):
                color = BUTTON_HOVER
            else:
                color = BUTTON_COLOR

            pygame.draw.rect(self.screen, color, rect, border_radius=6)

            label = self.font.render(algo, True, TEXT_COLOR)
            label_rect = label.get_rect(center=rect.center)
            self.screen.blit(label, label_rect)

        # Show current mode
        if planner:
            mode_text = self.font.render(
                f"Mode: {planner.mode}",
                True,
                TEXT_COLOR
            )
            self.screen.blit(mode_text,
                             (screen_w - SIDE_PANEL_WIDTH + 20, 80))
