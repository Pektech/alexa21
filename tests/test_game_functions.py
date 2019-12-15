import pytest
from lambda2.code.alexa import game_functions, cards
from lambda2.code.lambda_function import stand_handler


def test_hit(capsys):
    deck = cards.Deck()
    test_hand = cards.Hand()
    # set up a hand
    test_hand.hit(deck)
    test_hand.adjust_for_ace()
    test_hand.hit(deck)
    test_hand.adjust_for_ace()
    with capsys.disabled():
        print(test_hand.hand_held())

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


def test_alexa_dealing_herself():
    stand_handler()
    assert stand_handler() == "hmm"
