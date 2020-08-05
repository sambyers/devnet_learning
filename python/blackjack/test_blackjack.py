import unittest
from blackjack import BlackJack


class testBlackJack(unittest.TestCase):
    def setUp(self):
        self.players = ["me", "myself"]
        self.new_player = "New Player"
        self.house_player_name = "House"

    def test_players(self):
        game = BlackJack(self.players)
        self.assertEqual(game.players[0].name, self.players[0])

    def test_players_house(self):
        game = BlackJack(self.players)
        player_names = self._get_player_names(game)
        self.assertTrue(self.house_player_name in player_names)

    def test_get_player_names(self):
        game = BlackJack(self.players)
        player_names = game.player_names
        self.assertTrue(self.players[0] in player_names)

    def test_add_player(self):
        game = BlackJack(self.players)
        game.add_player(self.new_player)
        player_names = self._get_player_names(game)
        self.assertTrue(self.new_player in player_names)

    def test_deal_hand_to_players(self):
        game = BlackJack(self.players)
        game.deal_hand_to_players()
        self.assertTrue(game.players[0].hand.cards)

    def test_current_leader(self):
        game = BlackJack(self.players)
        game.deal_hand_to_players()
        test_player = game.current_leader
        self.assertIsInstance(test_player, object)

    def test_active_players(self):
        game = BlackJack(self.players)
        game.deal_hand_to_players()
        active = game.active_players
        self.assertTrue(active)

    def _get_player_names(self, game: object) -> list:
        player_names = []
        for player in game.players:
            player_names.append(player.name)
        return player_names
