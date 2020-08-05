"""
Janky Blackjack game done quickly for practice.
"""
from blackjack import BlackJack


##
# Game Blocks
##


def end_game(game):
    game.game_state = False
    print(f"GAME OVER -> The winner is {game.current_leader.name} 🍰")
    print("GAME OVER -> Thank you for playing!")


def game_status(game):
    print(f"BLACKJACK GAME -> {game}")
    for player in game.players:
        print(f'PLAYER INFO -> {player.name}, hand: {player.hand.cards} = {player.hand.hand_sum}')


def player_status(player):
    print(f"PLAYER INFO -> {player}")
    print(f"PLAYER INFO -> {player.hand.cards} = {player.hand.hand_sum}")


def check_for_natural(game):
    natural = False
    for player in game.players:
        if player.hand.natural:
            natural = True
    return natural


def turn_player(player):
    done = False
    while done is False:
        choice = input(
            f"PLAYER TURN -> {player.name}, would you like to hit, fold, or stay? (h/f/s) 🤔"
        )
        if "h" in choice.lower():
            hit = True
            while hit is True:
                if player.hand.busted():
                    print(f"PLAYER TURN -> Sorry {player.name}, your hand busted! 😵")
                    done = True
                    break
                print(f"PLAYER TURN -> Drawing a card for {player.name}...")
                player.hand.cards = player.hand.cards + game.deck.draw_cards(1)
                player_status(player)
                if not player.hand.busted():
                    hit_again = input("PLAYER TURN -> Hit again? (y/n) 🤔")
                    if "n" in hit_again.lower():
                        hit = False
                        done = True
                else:
                    print(f"PLAYER TURN -> Sorry {player.name}, your hand busted! 😵")
                    done = True
                    break
        elif "f" in choice.lower():
            print(f"PLAYER TURN -> Thanks for playing {player.name}!")
            player.hand.fold
            done = True
        elif "s" in choice.lower():
            print(f"PLAYER TURN ->{player.name} is staying!")
            done = True
        else:
            print("PLAYER TURN -> Not a valid choice! 👎")


if __name__ == "__main__":

    ##
    # Game Setup
    ##
    players = input("GAME SETUP -> Type in player names separated by a space: ")
    players = players.split(" ")
    game = BlackJack(players)
    game.deck.shuffle()
    game.deal_hand_to_players()

    if check_for_natural(game):
        print("BLACKJACK! -> We have a NATURAL! 🔥")
        end_game(game)

    ##
    # Main Game Loop
    ##
    while game.game_state:
        game_status(game)
        for player in game.active_players:
            turn_player(player)
        end_game(game)
