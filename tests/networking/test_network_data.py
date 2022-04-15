import unittest

from src.networking.network_data_base import NetworkData
from src.networking.network_data import *
from src.networking.network_commands import *

def test_pytest():
    assert type(NetworkData()) == NetworkData
    assert 2 == 2

def test_two():
    assert 1 == 1

class TestSum(unittest.TestCase):
    def test_from_json(self):
        """
        Test that it can transform any NetworkData subclass to a string
        """
        subclasses = [
            PlayerInfo("123"),
            GameState("123"),
            Message("123"),
            GetPlayerIDCommand(),
            GetGameStateCommand(),
            DisconnectPlayerCommand("123"),
            CreateGameCommand(),
            SendPlayerInput({"up": "123"}),
        ]
        
        for subclass in subclasses:
            result = subclass.to_json()
            self.assertIsInstance(result, str, msg=f"Failed to convert {subclass} to JSONified string")

