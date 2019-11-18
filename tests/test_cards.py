import pytest
from lambda2.code.alexa import cards


@pytest.fixture
def fake_card():
    fake_card = cards.Card("Diamonds", "King")
    return fake_card


def test_card2(fake_card):
    assert fake_card.suit == "Diamonds"
    assert fake_card.rank == "King"


def test_card():
    """Simple test for card object"""
    test_card = cards.Card("Diamonds", "King")
    assert test_card.suit == "Diamonds"
    assert test_card.rank == "King"


def test_deck():
    """Simple test that there are 52 cards in the deck"""
    test_deck = cards.Deck()
    assert len(test_deck.deck) == 52


def test_multiple_deck():
    """Simple test for multiple decks"""
    test_deck = cards.Deck(decks=2)

    assert len(test_deck.deck) == 104


def test_hand(fake_card, capsys):

    test_hand = cards.Hand()
    test_hand.add_cards(fake_card)
    print(test_hand)
    captured = capsys.readouterr()
    assert captured.out == "King of Diamonds, \n"


@pytest.mark.parametrize(
    "next_suit, next_rank, expected",
    [
        ("Diamonds", "King", 10),
        ("Hearts", "Ace", 21),
        ("Spades", "Eight", 29),
        ("Clubs", "Ace", 30),
    ],
)
def test_add_cards(next_suit, next_rank, expected):
    test_hand = cards.Hand()

    test_hand.add_cards(cards.Card(next_suit, next_rank))
    assert test_hand.value == expected
