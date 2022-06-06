import pygame
from controls.input_controls import (
    Controls,
    controllerInputHandler,
    general_controls,
    menu_controls,
)
from game.event_manager import (
    EventManager,
    GeneralControlInputEvent,
    InputEvent,
    PlayerInputEvent,
    QuitEvent,
    TickEvent,
    GetInputsEvent,
    MenuControlInputEvent,
)
from game.game import GameEngine


class Controller:
    """Handles all inputs from the users. Decoupled module from the GameEngine"""

    def __init__(self, evManager: EventManager, game: GameEngine):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.game = game

    def notify(self, event):
        """
        Receive events posted to the message queue.
        """
        if isinstance(event, GetInputsEvent):
            self.parse_input()

    def parse_input(self):
        # Read each input

        for event in pygame.event.get():
            # If the game is closed
            if event.type == pygame.QUIT:
                self.evManager.Post(QuitEvent())

            # If the event is a keypress
            if event.type == pygame.KEYDOWN:

                if self.game.state.in_menu and event.key in menu_controls:
                    self.evManager.Post(
                        MenuControlInputEvent(command=menu_controls[event.key])
                    )
                    break

                # Parse the keypress to a command
                if event.key in general_controls:
                    self.evManager.Post(
                        GeneralControlInputEvent(command=general_controls[event.key])
                    )
                    break

                # Receive player command
                for player in self.game.model.players:
                    if event.key in player.controls:
                        # NOTE sending the entire player, a problem? Seems the most easy, and its a reference so I don't see drawbacks right now.
                        self.evManager.Post(
                            PlayerInputEvent(
                                player=player, command=player.controls[event.key]
                            )
                        )

            # DO NOT REMOVE THIS CODE -- REMOVING CONTROLLER SUPPORT FOR NOW
            # TODO: This is needed to make the joystick work, but it makes no sense
            # This needs to be removed at some point (ideally)
            # joysticks = [
            #     pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())
            # ]
            # if event.type == pygame.JOYAXISMOTION or event.type == pygame.JOYHATMOTION:
            #     command = controllerInputHandler(event)
            #     if command != None and len(self.players) - 1 >= event.instance_id:
            #         self.players[event.instance_id + 1].set_command(command)
            # DO NOT REMOVE THIS CODE -- REMOVING CONTROLLER SUPPORT FOR NOW


# On the tickevent, controller reads all input.
# This input is then parsed from input device values to game control values (pygame.K_q -> Controls.QUIT)
# it filters these commands in high level --> if they are control commands (quit, pause) the appropriate events are send (why?)
# For the inputs that are game control inputs
# it posts an InputEvent() to the eventHandler for all inputs
# The game should then catch these events and translate them into game acts
# (How do we do this for multiple players?)
