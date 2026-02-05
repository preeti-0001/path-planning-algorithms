import pygame
import os
import json
from ui_pygame.screens.map_editor import MapEditor
from ui_pygame.screens.map_viewer import MapViewer


MAP_FOLDER = "maps"
FONT = None


class MapCard:
    def __init__(self, rect, name, is_add=False):
        self.rect = rect
        self.name = name
        self.is_add = is_add

    def draw(self, screen, font):
        color = (60, 60, 60)
        hover_color = (90, 90, 90)

        mouse = pygame.mouse.get_pos()
        fill = hover_color if self.rect.collidepoint(mouse) else color

        pygame.draw.rect(screen, fill, self.rect, border_radius=10)

        text = "+" if self.is_add else self.name
        label = font.render(text, True, (255, 255, 255))
        text_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, text_rect)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


class HomeScreen:
    def __init__(self, screen):
        global FONT
        self.screen = screen
        self.width, self.height = screen.get_size()

        FONT = pygame.font.SysFont("arial", 24)

        self.cards = []
        self.load_maps()
        self.build_grid()

    def load_maps(self):
        if not os.path.exists(MAP_FOLDER):
            os.makedirs(MAP_FOLDER)

        self.map_names = []

        for file in os.listdir(MAP_FOLDER):
            if file.endswith(".json"):
                path = os.path.join(MAP_FOLDER, file)

                try:
                    with open(path, "r") as f:
                        content = f.read().strip()

                        if not content:
                            print(f"Skipping empty file: {file}")
                            continue

                        data = json.loads(content)
                        self.map_names.append(data.get("name", file))

                except json.JSONDecodeError:
                    print(f"Invalid JSON, skipping: {file}")

    def build_grid(self):
        self.cards = []

        padding = 40
        cols = 4
        card_w = 200
        card_h = 100
        spacing = 30

        x0 = padding
        y0 = 120

        items = self.map_names + ["ADD"]

        for i, name in enumerate(items):
            row = i // cols
            col = i % cols

            x = x0 + col * (card_w + spacing)
            y = y0 + row * (card_h + spacing)

            rect = pygame.Rect(x, y, card_w, card_h)

            card = MapCard(rect, name, is_add=(name == "ADD"))
            self.cards.append(card)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            for card in self.cards:
                if card.clicked(pos):
                    if card.is_add:
                        print("Opening editor")
                        return MapEditor(self.screen)
                    else:
                        print("Opening file")
                        return MapViewer(self.screen, card.name)

        return None

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill((30, 30, 30))

        title = FONT.render("Select Map", True, (255, 255, 255))
        self.screen.blit(title, (40, 40))

        for card in self.cards:
            card.draw(self.screen, FONT)
