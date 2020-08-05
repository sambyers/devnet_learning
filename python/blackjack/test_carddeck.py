import unittest
from carddeck import CardDeck


class testCardDeck(unittest.TestCase):
    def setUp(self):
        self.default_first_card = "Ace of Clubs"
        self.test_cards = ["Ace of Clubs", "2 of Clubs"]
        self.test_card_deck = ("Ace of Clubs", "2 of Clubs")
        self.hand_size = 2

    def test_deck_starting_cards(self):
        deck = CardDeck()
        self.assertEqual(deck.cards[0], self.default_first_card)

    def test_deck_shuffle(self):  # How do you test random?? haha
        deck = CardDeck()
        deck.shuffle()
        self.assertTrue(deck.shuffled)

    def test_deck_reset_cards(self):
        deck = CardDeck()
        deck.cards = ()
        deck.reset_cards()
        self.assertEqual(deck.cards[0], self.default_first_card)

    def test_deck_draw_card(self):
        deck = CardDeck()
        card = deck.draw_card()
        self.assertEqual(card, self.default_first_card)

    def test_deck_draw_cards(self):
        deck = CardDeck()
        deck.cards = self.test_card_deck
        hand = deck.draw_cards(self.hand_size)
        self.assertEqual(self.test_cards, hand)
