import pygame
from ui_pygame.screens.home_screen import HomeScreen

WIDTH, HEIGHT = 1000, 700

def run_app():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Robot Path Lab")

    clock = pygame.time.Clock()

    current_screen = HomeScreen(screen)

    running = True
    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            next_screen = current_screen.handle_event(event)

            if next_screen:
                current_screen = next_screen

        current_screen.update(dt)
        current_screen.draw()

        pygame.display.flip()

    pygame.quit()
