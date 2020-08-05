import unittest
from hand import Hand
from unittest.mock import MagicMock, patch


class testHand(unittest.TestCase):
    def setUp(self):
        self.test_card = ["3 of Clubs"]
        self.test_cards = ["Ace of Clubs", "2 of Clubs"]
        self.test_card_natural = ["Ace of Clubs", "Queen of Clubs"]
        self.test_cards_busted = ["King of Clubs", "Queen of Clubs", "6 of Clubs"]
        self.test_cards_ace_as_one = ["Ace of Clubs", "2 of Clubs", "9 of Clubs"]

    def test_hand(self):
        hand = Hand(self.test_cards)
        self.assertTrue(
            self.test_cards[0] in hand.cards[0] and self.test_cards[1] in hand.cards[1]
        )

    def test_hand_sum(self):
        hand = Hand(self.test_cards)
        self.assertEqual(hand.hand_sum, 13)

    def test_hand_sum_ace_as_one(self):
        hand = Hand(self.test_cards_ace_as_one)
        self.assertEqual(hand.hand_sum, 12)

    def test_hand_not_busted(self):
        hand = Hand(self.test_cards)
        self.assertFalse(hand.busted())

    def test_hand_busted(self):
        hand = Hand(self.test_cards_busted)
        self.assertTrue(hand.busted())

    def test_add_card_to_hand(self):
        hand = Hand(self.test_cards)
        hand.cards = hand.cards + self.test_card
        self.assertEqual(len(hand.cards), len(self.test_cards + self.test_card))

    def test_natural_false(self):
        hand = Hand(self.test_cards)
        self.assertFalse(hand.natural)

    def test_natural_true(self):
        hand = Hand(self.test_card_natural)
        self.assertTrue(hand.natural)

    def test_fold(self):
        hand = Hand(self.test_cards)
        hand.fold()
        self.assertFalse(hand.cards)

    def test_card_count(self):
        hand = Hand(self.test_cards)
        self.assertTrue(hand.card_count > 0)

    def test_valid(self):
        hand = Hand(self.test_cards)
        self.assertTrue(hand.valid)

    @patch("player.Player")
    def test_attach(self, Player):
        player = Player()
        player.update = MagicMock(return_value=None)
        hand = Hand(self.test_cards)
        hand.attach(player)
        self.assertTrue(len(hand.subscribers) > 0)

    @patch("player.Player")
    def test_detach(self, Player):
        player = Player()
        player.update = MagicMock(return_value=None)
        hand = Hand(self.test_cards)
        hand.subscribers.append(player)
        hand.detach(player)
        self.assertEqual(len(hand.subscribers), 0)
