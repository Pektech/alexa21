import pytest
from lambda2.code.alexa import cards
from lambda2.code import game_set_up as gm


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
    """test that hand displays correctly"""
    test_hand = cards.Hand()
    test_hand.add_cards(fake_card)
    assert test_hand.hand_held() == "King of Diamonds"


def test_add_cards1():
    """Adding cards to hand gives correct hand value"""
    test_hand = cards.Hand()

    test_hand.add_cards(cards.Card("Diamonds", "King"))
    assert test_hand.value == 10
    assert test_hand.aces == 0


def test_add_cards2():
    """Next 5 tests are checking aces are handled correctly"""
    test_hand = cards.Hand()
    test_hand.add_cards(cards.Card("Diamonds", "King"))
    test_hand.adjust_for_ace()
    test_hand.add_cards(cards.Card("Hearts", "Ace"))
    test_hand.adjust_for_ace()

    assert test_hand.value == 21
    assert test_hand.aces == 1


def test_add_cards3():
    test_hand = cards.Hand()
    test_hand.add_cards(cards.Card("Diamonds", "King"))
    test_hand.adjust_for_ace()
    test_hand.add_cards(cards.Card("Hearts", "Ace"))
    test_hand.adjust_for_ace()
    test_hand.add_cards(cards.Card("Spades", "Eight"))
    test_hand.adjust_for_ace()

    assert test_hand.value == 19
    assert test_hand.aces == 0


def test_add_cards4():
    test_hand = cards.Hand()
    test_hand.add_cards(cards.Card("Diamonds", "King"))
    test_hand.adjust_for_ace()
    test_hand.add_cards(cards.Card("Hearts", "Ace"))
    test_hand.adjust_for_ace()
    test_hand.add_cards(cards.Card("Spades", "Eight"))
    test_hand.adjust_for_ace()
    test_hand.add_cards(cards.Card("Clubs", "Ace"))
    test_hand.adjust_for_ace()

    assert test_hand.value == 20
    assert test_hand.aces == 0


def test_add_cards5():
    test_hand = cards.Hand()

    test_hand.add_cards(cards.Card("Hearts", "Ace"))
    test_hand.adjust_for_ace()

    test_hand.add_cards(cards.Card("Clubs", "Ace"))
    test_hand.adjust_for_ace()

    assert test_hand.value == 12
    assert test_hand.aces == 1


def test_add_cards6():
    test_hand = cards.Hand()

    test_hand.add_cards(cards.Card("Hearts", "Ace"))
    test_hand.adjust_for_ace()

    test_hand.add_cards(cards.Card("Clubs", "Ace"))
    test_hand.adjust_for_ace()

    test_hand.add_cards(cards.Card("Clubs", "Ace"))
    test_hand.adjust_for_ace()

    assert test_hand.value == 13
    assert test_hand.aces == 1


def test_deal(capsys):
    deck = cards.Deck()
    test_hit = deck.deal()
    print(test_hit)
    captured = capsys.readouterr()
    assert captured.out == "Ace of Clubs\n"


def test_holding():
    test_hand = cards.Hand()
    test_hand.add_cards(cards.Card("Diamonds", "King"))
    test_hand.adjust_for_ace()
    test_hand.add_cards(cards.Card("Hearts", "Ace"))
    test_hand.adjust_for_ace()
    test_hand.add_cards(cards.Card("Spades", "Eight"))
    test_hand.adjust_for_ace()
    assert test_hand.holding() == [
        ("Diamonds", "King"),
        ("Hearts", "Ace"),
        ("Spades", "Eight"),
    ]
    assert test_hand.cards[0].rank == "King"


@pytest.mark.skip("not working yet")
def test_converting_list_to_object():
    test_hand = cards.Hand()
    test_alexa_session_attr = ["King of Diamonds", "Ace of Hearts", "Eight of Spades"]
    pass


def test_card_string():
    test_hand = cards.Hand()
    test_hand.add_cards(cards.Card("Diamonds", "King"))
    test_hand.adjust_for_ace()
    assert test_hand.hand_held() == "King of Diamonds"
    test_hand.add_cards(cards.Card("Hearts", "Ace"))
    test_hand.adjust_for_ace()
    assert test_hand.hand_held() == "King of Diamonds, and the Ace of Hearts"
    test_hand.add_cards(cards.Card("Spades", "Eight"))
    test_hand.adjust_for_ace()
    assert (
        test_hand.hand_held()
        == "King of Diamonds, Ace of Hearts, and the Eight of Spades"
    )


def test_create_initial_hands():
    test_player, test_alexa = gm.player_hand, gm.alexa_hand
    print(test_player.hand_held(), test_alexa.hand_held())
    assert test_player != test_alexa
