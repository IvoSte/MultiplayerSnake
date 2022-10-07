import pygame
import model
from eventmanager import InitializeEvent, QuitEvent, TickEvent


class GraphicalView(object):
    """
    Draws the model state onto the screen.
    """

    def __init__(self, evManager, model):
        """_summary_

        Args:
            evManager (EventManager): Allows posting messages to the event queue.
            model (GameEngine): a strong reference to the game Model.

        Attributes:
        isinitialized (bool): pygame is ready to draw.
        screen (pygame.Surface): the screen surface.
        clock (pygame.time.Clock): keeps the fps constant.
        smallfont (pygame.Font): a small font.
        """

        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model
        self.isinitialized = False
        self.screen = None
        self.clock = None
        self.smallfont = None

    def notify(self, event):
        """
        Receive events posted to the message queue.
        """
        if isinstance(event, InitializeEvent):
            self.initialize()
        if isinstance(event, QuitEvent):
            # shut down the pygame graphics
            self.isinitialized = False
            pygame.quit()
        elif isinstance(event, TickEvent):
            self.renderall()
            # limit the redraw speed to 30 frames per second
            self.clock.tick(30)

    def renderall(self):
        """
        Draw the current game state on screen.
        Does nothing if isinitialized == False (pygame.init failed)
        """
        if not self.isinitialized:
            return
        # clear screen
        # render call for background
        # render call for entities
        # render call for UI elements
        # ...

    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """
        result = pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((600, 60))
        self.clock = pygame.time.Clock()
        self.smallfont = pygame.font.Font(None, 40)
        self.isinitialized = True
