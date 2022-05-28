from dataclasses import dataclass

from controls.input_controls import Controls
from entities.snake import Snake


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
class PlayerInputEvent(Event):
    name: str = "Player input event"
    player: Snake = None
    command: Controls = None


@dataclass
class GetInputsEvent(Event):
    name: str = "Get inputs event"
    data = None


@dataclass
class GeneralControlInputEvent(Event):
    name: str = "General control input event"
    command: Controls = None


@dataclass
class MenuControlInputEvent(Event):
    name: str = "Menu control input event"
    command: Controls = None


@dataclass
class InitializeEvent(Event):
    name: str = "Initialize event"


@dataclass
class GamePausedEvent(Event):
    name: str = "Game paused event"


@dataclass
class RestartGameEvent(Event):
    name: str = "Restart game event"


@dataclass
class GameEndedEvent(Event):
    name: str = "Game ended event"


class EventManager:
    """
    Coordinates communication between the Model, View and Controller
    """

    def __init__(self):
        from weakref import WeakKeyDictionary, WeakSet

        # Using weak key references allows the garbage collector to destroy the object when all strong references to the object are gone.
        # The large objects will not continue to live in the cache when they are not used anymore. (like Rust)
        self.listeners = WeakKeyDictionary()
        self.listenerBuffer = WeakSet()

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

        if not isinstance(event, TickEvent) and not isinstance(event, GetInputsEvent):
            # print the event unless it is a TickEvent or getInpuntsEvent
            print(event)
        for listener in self.listeners:
            listener.notify(event)