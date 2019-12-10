import pytest
from lambda2.code.alexa import game_functions, cards


def test_hit(capsys):
    deck = cards.Deck()
    hand = cards.Hand()
    # set up a hand
    hand.add_cards(cards.Card("Clubs", "Ten"))
    test_hand = game_functions.hit(deck, hand)
    # print(test_hand)
    # captured = capsys.readouterr()
    assert test_hand.value == 21


def test_isbust(capsys):
    hand = cards.Hand()

    hand.add_cards(cards.Card("Clubs", "Ten"))
    print(hand.value)

    assert game_functions.isbust(hand) is False
    hand.add_cards(cards.Card("Clubs", "Eight"))
    print(hand.value)

    assert game_functions.isbust(hand) is False
    hand.add_cards(cards.Card("Clubs", "Ace"))
    print(hand.value)

    assert game_functions.isbust(hand) is False
    hand.add_cards(cards.Card("Clubs", "Four"))
    print(hand.value)

    assert game_functions.isbust(hand) is True


def test_player_loses_bet():

    chips = 100
    bet = 10
    assert chips - bet == game_functions.player_loses_bet(bet, chips)
