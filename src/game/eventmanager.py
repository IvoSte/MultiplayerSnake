from dataclasses import dataclass


@dataclass
class Event:
    """
    A superclass for any events that might be generated by an
    object and sent to the EventManager.
    """
    name: str = "Generic event"


@dataclass
class QuitEvent(Event):
    name: str = "Quit event"


@dataclass
class TickEvent(Event):
    name: str = "Tick event"


@dataclass
class InputEvent(Event):
    name: str = "Input event"
    keyboardkey: str = None
    clickpos: tuple = None
    controllerbutton: str = None
    controlleraxismotion: str = None


@dataclass
class InitializeEvent(Event):
    name: str = "Initialize event"


class EventManager:
    """
    Coordinates communication between the Model, View and Controller
    """

    def __init__(self):
        from weakref import WeakKeyDictionary

        # Using weak key references allows the garbage collector to destroy the object when all strong references to the object are gone.
        # The large objects will not continue to live in the cache when they are not used anymore. (like Rust)
        self.listeners = WeakKeyDictionary()

    def RegisterListener(self, listener):
        """
        Adds a listener to our message queue.
        It will receive Post()ed events through its notify(event) call.
        """
        # huh why use a dict if we don't want to use the value? Why not use a weak set or something?
        self.listeners[listener] = 1

    def UnregisterListener(self, listener):
        """
        Remove a listener from our spam list.
        This is implemented but hardly used.
        Our weak ref spam list will auto remove any listeners who stop existing.
        """
        if listener in self.listeners:
            del self.listeners[listener]

    def Post(self, event):
        """
        Post a new event to the message queue.
        It will be broadcast to all listeners.
        """

        if not isinstance(event, TickEvent):
            # print the event unless it is a TickEvent
            print(event)
        for listener in self.listeners:
            listener.notify(event)
