from cardvalues import card_values


class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.max_score = 21
        self.subscribers = []

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, cards: list):
        self._cards = cards

    @property
    def valid(self):
        if self.hand_sum <= self.max_score and self.card_count > 0:
            return True
        else:
            return False

    @property
    def hand_sum(self) -> int:
        hand_sum = sum([card_values[card] for card in self.cards])
        if "Ace" in str(self.cards) and hand_sum > self.max_score:
            return hand_sum - 10
        else:
            return hand_sum

    @property
    def natural(self) -> bool:
        if self.hand_sum == self.max_score:
            return True
        else:
            return False

    def busted(self) -> bool:
        if self.hand_sum > self.max_score:
            self.fold()
            self.notify()
            return True
        else:
            return False

    @property
    def card_count(self) -> int:
        return len(self.cards)

    def fold(self) -> None:
        self.cards = []

    def notify(self):
        for sub in self.subscribers:
            sub.update(self)

    def attach(self, subscriber):
        self.subscribers.append(subscriber)

    def detach(self, subscriber):
        self.subscribers.remove(subscriber)

    def __repr__(self):
        return f"Cards: {self.cards}, Hand Sum: {self.hand_sum}, Valid: {self.valid}"
