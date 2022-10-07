import pygame
from eventmanager import QuitEvent, InitializeEvent, TickEvent


class GameEngine(object):
    """
    Tracks the game state.
    """

    def __init__(self, evManager):
        """_summary_

        Args:
            evManager (EventManager): Allows posting messages to the event queue.
        """

        self.evManager = evManager
        evManager.RegisterListener(self)
        self.running = False

    def notify(self, event):
        """
        Called by an event in the message queue
        """

        if isinstance(event, QuitEvent):
            self.running = False

    def run(self):
        """
        Starts the game engine loop.
        This pumps a Tick event into the message queue for each loop.
        The loop ends when thios object hears a QuitEvent in notify().
        """
        self.running = True
        self.evManager.Post(InitializeEvent())
        while self.running:
            newTick = TickEvent()
            self.evManager.Post(newTick)