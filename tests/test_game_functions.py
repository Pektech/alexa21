import pytest
from lambda2.code.alexa import game_functions as gf, cards
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

    assert gf.isbust(hand) is False
    hand.add_cards(cards.Card("Clubs", "Eight"))
    print(hand.value)

    assert gf.isbust(hand) is False
    hand.add_cards(cards.Card("Clubs", "Ace"))
    print(hand.value)

    assert gf.isbust(hand) is False
    hand.add_cards(cards.Card("Clubs", "Four"))
    print(hand.value)

    assert gf.isbust(hand) is True


def test_player_loses_bet():
    chips = 100
    bet = 10
    assert chips - bet == gf.player_loses_bet(bet, chips)


test_data = [(17, 17, False), (17, 16, True), (18, 19, False), (18, 24, False)]


@pytest.mark.parametrize("test_player_value, test_alexa_value, expected", test_data)
def test_should_alexa_hit(test_player_value, test_alexa_value, expected):
    test_player_hand = cards.Hand()
    test_alexa_hand = cards.Hand()
    test_player_hand.value = test_player_value
    test_alexa_hand.value = test_alexa_value

    assert gf.should_alexa_hit(test_player_hand, test_alexa_hand) is expected


test_bets = [(10, 100, True), (100, 10, False), (100, 100, True)]


@pytest.mark.parametrize("bet, chips_total, expected", test_bets)
def test_can_bet(bet, chips_total, expected):
    test_chips = cards.Chips()
    test_chips.total = chips_total

    assert gf.can_bet(bet, test_chips) is expected
