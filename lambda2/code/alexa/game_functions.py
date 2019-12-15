from lambda2.code.alexa import cards


# def hit(deck, hand):
#
#     card = deck.deal()
#     print(card)
#     hand.add_cards(cards.Card(card.suit, card.rank))
#
#     return hand


def isbust(hand):

    if hand.value > 21:
        return True
    else:
        return False


def player_loses_bet(bet, player_chips):
    return player_chips - bet


# just for testing alexa dealing and winning
