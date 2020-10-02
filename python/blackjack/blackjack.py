from player import Player
from carddeck import CardDeck
from hand import Hand


class BlackJack:
    def __init__(self, players: list):
        self.game_state = True
        self.players = players
        self.hand_size = 2
        self.deck = CardDeck()
        self.winning_score = 21

    @property
    def players(self) -> list:
        return self._players

    @players.setter
    def players(self, players: list) -> None:
        player_objs = []
        for player in players:
            player_obj = Player(player)
            player_objs.append(player_obj)
        house_player = Player("House")
        player_objs.append(house_player)
        self._players = player_objs

    @property
    def player_names(self) -> list:
        players = self.players
        player_names = []
        for player in players:
            player_names.append(player.name)
        return player_names

    @property
    def current_leader(self) -> Player:
        return max(self.active_players, key=lambda player: player.hand.hand_sum)

    def add_player(self, name: str) -> None:
        new_player = Player(name)
        self.players.append(new_player)

    def deal_hand_to_players(self) -> None:
        for player in self.players:
            player.hand = Hand(self.deck.draw_cards(self.hand_size))
            player.hand.attach(player)

    def clean_up_busted_hands(self) -> list:
        players = []
        for player in self.active_players:
            busted = player.hand.busted()
            if busted:
                players.append(player)
        return players

    @property
    def active_players(self) -> list:
        return [player for player in self.players if player.active]

    def __repr__(self):
        return f"Players: {self.player_names}, Game State: {self.game_state}"
