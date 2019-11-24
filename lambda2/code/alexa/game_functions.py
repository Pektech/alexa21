def hit(deck, hand):

    card = deck.deal()
    hand.add_cards(card)

    return hand


def IsBust(hand):

    if hand.value > 21:
        return True
    else:
        return False
