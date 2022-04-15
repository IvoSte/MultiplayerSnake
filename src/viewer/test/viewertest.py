import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


class Viewer():
    def __init__(self):
        self.display = pygame.display.set_mode((800, 800))
        self.surface_1 = pygame.Surface((400, 400))
        self.surface_2 = pygame.Surface((400, 400))

    def clear_screen(self):
        self.display.fill(pygame.Color(0, 0, 200))

    def draw(self):
        self.clear_screen()
        rect = pygame.draw.rect(self.surface_1, pygame.Color(200,0,0), [200, 300, 250, 350])
        rect2 = pygame.draw.rect(self.surface_2, pygame.Color(0,200,0), [20, 30, 25, 35])
        self.display.blit(self.surface_1, [0,0])
        self.display.blit(self.surface_2, [400,400])


    def update(self):
        pygame.display.update()

def main():
    pygame.init()
    viewer = Viewer()
    viewer.draw()
    viewer.update()
    # Variable to keep the main loop running
    running = True

    # Main loop
    while running:
        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    running = False

            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                running = False

if __name__ == "__main__":
    main()