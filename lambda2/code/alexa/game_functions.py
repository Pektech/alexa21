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


def should_alexa_hit(player_hand, alexa_hand):
    return (
        21 >= alexa_hand.value
        and alexa_hand.value < player_hand.value
        and not isbust(alexa_hand)
    )


def can_bet(bet, player_chips):
    return bet <= player_chips.total
