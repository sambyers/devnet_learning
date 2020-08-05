import unittest
from player import Player
from unittest.mock import PropertyMock, patch


class testPlayer(unittest.TestCase):
    def setUp(self):
        self.player_name = "test"
        self.test_cards = ["Ace of Clubs", "2 of Clubs"]

    def test_player_name(self):
        player = Player(self.player_name)
        self.assertEqual(player.name, self.player_name)

    def test_player_hand(self):
        player = Player(self.player_name)
        player.hand = self.test_cards
        self.assertEqual(player.hand, self.test_cards)

    def test_player_active_true(self):
        player = Player(self.player_name)
        player.hand = self.test_cards
        self.assertTrue(player.active)

    def test_player_active_false(self):
        player = Player(self.player_name)
        self.assertFalse(player.active)

    @patch("hand.Hand")
    def test_player_update(self, Hand):
        hand = Hand()
        valid = PropertyMock(return_value=False)
        type(hand).valid = valid
        player = Player(self.player_name)
        player.hand = Hand()
        player.update(hand)
        self.assertEqual(player.hand, None)
