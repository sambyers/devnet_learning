import random
from cards import initial_card_deck


class CardDeck:
    def __init__(self):
        self.shuffled = False
        self.starting_cards = initial_card_deck
        self.cards = self.starting_cards

    @property
    def cards(self) -> list:
        return self._cards

    @cards.setter
    def cards(self, cards: tuple):
        self._cards = list(cards)

    def reset_cards(self) -> None:
        self.cards = self.starting_cards
        self.shuffled = False

    def shuffle(self) -> bool:
        cards = self.cards
        count = len(cards)
        for i in range(count):
            randindex = random.randrange(count)
            cards[i], cards[randindex] = cards[randindex], cards[i]
        self.cards = cards
        self.shuffled = True
        return self.shuffled

    def draw_card(self) -> str:
        return self.cards.pop(0)

    def draw_cards(self, size: int) -> list:
        hand = []
        for i in range(size):
            hand.append(self.draw_card())
        return hand

    def __repr__(self):
        return f"Cards: {self.cards}, Shuffled: {self.shuffled}"
