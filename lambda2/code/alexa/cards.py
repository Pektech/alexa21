import random


suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = (
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Jack",
    "Queen",
    "King",
    "Ace",
)
values = {
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    "Six": 6,
    "Seven": 7,
    "Eight": 8,
    "Nine": 9,
    "Ten": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10,
    "Ace": 11,
}


class Card:
    def __init__(self, suit, rank):

        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self, decks=1):
        self.deck = []
        self.decks = decks
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
        self.deck = self.deck * decks

    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += "\n " + card.__str__()
        return deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_cards(self, card):
        self.cards.append(card)
        if card.rank == "Ace":
            self.aces += 1
        self.value += values[card.rank]
        self.adjust_for_ace()

    def hand_held(self):
        hand_held = ""
        hand_list = self.holding()
        if len(hand_list) == 1:
            hand_held = hand_list[0][1] + " of " + hand_list[0][0]
            return hand_held
        else:
            for card in hand_list[:-1]:
                hand_held += card[1] + " of " + card[0] + ", "
            hand_held += "and the " + hand_list[-1][1] + " of " + hand_list[-1][0]
        return hand_held

    def holding(self):
        cards_held = []
        for card in self.cards:
            cards_held.append((card.suit, card.rank))
        return cards_held

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def create_initial_hand(self) -> object:
        player_hand = Hand()
        alexa_hand = Hand()
        game_deck = Deck()
        game_deck.shuffle()
        player_hand.add_cards(game_deck.deal())
        alexa_hand.add_cards(game_deck.deal())
        player_hand.add_cards(game_deck.deal())
        alexa_hand.add_cards(game_deck.deal())
        return player_hand, alexa_hand, game_deck

    def hit(self, game_deck):
        card = game_deck.deal()
        self.add_cards(Card(card.suit, card.rank))
        return self

    def clear_hand(self):
        self.cards = []
        return self

    @staticmethod
    def new_deal(player_hand, alexa_hand, game_deck):
        player_hand.hit(game_deck)
        alexa_hand.hit(game_deck)
        player_hand.hit(game_deck)
        alexa_hand.hit(game_deck)
        return player_hand, alexa_hand


class Chips:
    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


class GameState:
    def __init__(self):
        self.state = "Ready"
