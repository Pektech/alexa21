from lambda2.code.alexa import cards

player_hand, alexa_hand, deck = cards.Hand().create_initial_hand()

game_state = cards.GameState()

player_chips = cards.Chips()
