class Player:
    def __init__(self, name: str):
        self.name = name
        self._hand = None

    @property
    def hand(self) -> Hand:
        return self._hand

    @hand.setter
    def hand(self, hand: Hand):
        self._hand = hand

    @property
    def active(self) -> bool:
        if self.hand:
            return True
        else:
            return False

    def update(self, hand):
        if hand.valid:
            pass
        else:
            self.hand = None

    def __repr__(self):
        return f"Player: {self.name}, Active: {self.active}"
