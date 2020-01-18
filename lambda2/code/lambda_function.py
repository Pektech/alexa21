import json
import logging

from ask_sdk_core.skill_builder import SkillBuilder, CustomSkillBuilder
from ask_sdk_core.api_client import DefaultApiClient
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.serialize import DefaultSerializer
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler,
    AbstractExceptionHandler,
    AbstractResponseInterceptor,
    AbstractRequestInterceptor,
)
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_core.response_helper import get_plain_text_content, get_rich_text_content

from ask_sdk_model.interfaces.display import (
    ImageInstance,
    Image,
    RenderTemplateDirective,
    ListTemplate1,
    BackButtonBehavior,
    ListItem,
    BodyTemplate2,
    BodyTemplate1,
)
from ask_sdk_model import (
    ui,
    Response,
    DialogState,
    Intent,
    SlotConfirmationStatus,
    Slot,
    IntentConfirmationStatus,
)
from ask_sdk_model.ui import simple_card, SimpleCard
from ask_sdk_model.dialog import ElicitSlotDirective, DelegateDirective
from ask_sdk_model.services.directive import (
    SendDirectiveRequest,
    Header,
    SpeakDirective,
    DirectiveServiceClient,
)

from lambda2.code.alexa import data, cards, game_functions
from lambda2.code import game_set_up as gm

# Skill builder object

sb = CustomSkillBuilder(api_client=DefaultApiClient())

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# request handlers launch bstython with bstpy lambda2.code.lambda_function.handler

# start game
# player_hand, alexa_hand, deck = cards.Hand().create_initial_hand()


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch.
     """

    # set up deck and initial hand

    # player_hand, alexa_hand, deck = cards.Hand().create_initial_hand()
    speech_text = data.WELCOME
    # Set session attributes for the game
    game_session_attr = handler_input.attributes_manager.session_attributes
    if not game_session_attr:
        game_session_attr["GAME_STATE"] = 0
        game_session_attr["CHIPS"] = gm.player_chips.total
        game_session_attr["last_speech"] = speech_text
    print(gm.alexa_hand.holding())

    return (
        handler_input.response_builder.speak(speech_text)
        .ask(game_session_attr["last_speech"])
        .set_card(SimpleCard("Simple 21", speech_text))
        .set_should_end_session(False)
        .response
    )


@sb.request_handler(can_handle_func=is_intent_name("ReadyGame"))
def start_game(handler_input):
    game_session_attr = handler_input.attributes_manager.session_attributes
    game_session_attr["GAME_STATE"] = "RUNNING"
    # player_hand = game_session_attr["PLAYER"]
    gm.game_state.state = "Playing"
    p_hand = gm.player_hand.hand_held()
    a_hand = gm.alexa_hand.holding()
    print("alexa: ", gm.alexa_hand.holding())
    print("player: ", gm.player_hand.holding())
    output = f"""Now we can start the game. I'll deal. You have {p_hand}.
    I have a {a_hand[1][1]} of {a_hand[1][0]} showing. how much would you like to bet?"""
    # handler_input.response_builder.add_directive(
    #     DelegateDirective(updated_intent=Intent(name='Betting')))
    return (
        handler_input.response_builder.speak(output)
        .set_should_end_session(False)
        .response
    )


# this intent handles the bet and has a required slot


@sb.request_handler(can_handle_func=is_intent_name("Betting"))
def bet_handler(handler_input):
    # handles that a bet has been set and remembers amount
    request_id_holder = handler_input.request_envelope.request.request_id
    directive_header = Header(request_id=request_id_holder)
    slots = handler_input.request_envelope.request.intent.slots

    bet = slots["amount"].value
    gm.player_chips.bet = int(bet)
    if not game_functions.can_bet(gm.player_chips.bet, gm.player_chips):
        output = f"""Sorry but you do not have enough for that bet.  You have a total of 
        {gm.player_chips.total}, how much would you like to bet?"""
        # speech = SpeakDirective(speech=output)
        # directive_request = SendDirectiveRequest(
        #     header=directive_header, directive=speech
        # )
        # directive_service_client = (
        #     handler_input.service_client_factory.get_directive_service()
        # )
        # directive_service_client.enqueue(directive_request)

        return (
            handler_input.response_builder.speak(output)
            .add_directive(
                ElicitSlotDirective(
                    slot_to_elicit="amount",
                    updated_intent=Intent(
                        name="Betting",
                        confirmation_status=IntentConfirmationStatus.NONE,
                        slots={
                            "amount": Slot(
                                name="amount",
                                confirmation_status=SlotConfirmationStatus.NONE,
                            )
                        },
                    ),
                )
            )
            .response
        )

    p_hand = gm.player_hand.hand_held()
    a_hand = gm.alexa_hand.holding()
    print("alexa: ", gm.alexa_hand.holding())
    print("player: ", gm.player_hand.holding())
    print("chips : ", gm.player_chips.total, "bet :", gm.player_chips.bet)
    output = f"""Okay you bet {bet}. You have {p_hand}.
    I have a {a_hand[1][1]} of {a_hand[1][0]} showing. What you like to  Hit or Stand?"""

    return (
        handler_input.response_builder.speak(output)
        .set_should_end_session(False)
        .response
    )


@sb.request_handler(can_handle_func=is_intent_name("Hit"))
def play_handler(handler_input):
    game_session_attr = handler_input.attributes_manager.session_attributes
    print("alexa: ", gm.alexa_hand.holding())
    print("player: ", gm.player_hand.holding())

    # add card to player hands
    gm.player_hand.hit(gm.deck)
    print(gm.player_hand.holding())
    # check if bust
    if not game_functions.isbust(gm.player_hand):
        current_hand = gm.player_hand.hand_held()
        output = f""" You have {current_hand}, would you like to hit or stand?"""
        return (
            handler_input.response_builder.speak(output)
            .set_should_end_session(False)
            .response
        )
    else:
        return stand_handler(handler_input)
        # output = "Sorry you bust. My turn"
        # return (
        #     handler_input.response_builder.speak(output)
        #     .set_should_end_session(False)
        #     .response
        # )
    # ask hit or stand. if stand deal cards to alexa


# stand which lets alexa deal till higher than 17
@sb.request_handler(can_handle_func=is_intent_name("Stand"))
def stand_handler(handler_input):
    request_id_holder = handler_input.request_envelope.request.request_id
    directive_header = Header(request_id=request_id_holder)
    if game_functions.isbust(gm.player_hand):
        output = f"""Sorry you bust with a total of {gm.player_hand.value}. My Turn"""
        speech = SpeakDirective(speech=output)
        directive_request = SendDirectiveRequest(
            header=directive_header, directive=speech
        )
        directive_service_client = (
            handler_input.service_client_factory.get_directive_service()
        )
        directive_service_client.enqueue(directive_request)
    print("alexa: ", gm.alexa_hand.holding())
    print("player: ", gm.player_hand.holding())
    while game_functions.should_alexa_hit(gm.player_hand, gm.alexa_hand):
        gm.alexa_hand.hit(gm.deck)
        current_hand = gm.alexa_hand.hand_held()

        output = f""" I have {current_hand}"""
        speech = SpeakDirective(speech=output)
        directive_request = SendDirectiveRequest(
            header=directive_header, directive=speech
        )
        directive_service_client = (
            handler_input.service_client_factory.get_directive_service()
        )
        directive_service_client.enqueue(directive_request)

        print("alexa: ", gm.alexa_hand.holding())
        print("player: ", gm.player_hand.holding())
        print("chips: ", gm.player_chips.total)
        # check if alexa has bust
        if gm.alexa_hand.value > 21:
            gm.player_chips.win_bet()
            output = f"I bust so You won. Play again?"
            print("chips : ", gm.player_chips.total)
            return (
                handler_input.response_builder.speak(output)
                .set_should_end_session(False)
                .response
            )
    # if alexa is less than player, player wins, add winnings, draw new cards
    if gm.alexa_hand.value < gm.player_hand.value:

        gm.player_chips.win_bet()
        output = f"You won. Play again?"
        print("alexa: ", gm.alexa_hand.holding())
        print("player: ", gm.player_hand.holding())
        print("chips: ", gm.player_chips.total)
        return (
            handler_input.response_builder.speak(output)
            .set_should_end_session(False)
            .response
        )
    elif gm.alexa_hand.value > gm.player_hand.value:
        gm.player_chips.lose_bet()
        output = f"You lost. Play again?"
        print("alexa: ", gm.alexa_hand.holding())
        print("player: ", gm.player_hand.holding())
        print("chips: ", gm.player_chips.total)
        return (
            handler_input.response_builder.speak(output)
            .set_should_end_session(False)
            .response
        )
    else:
        output = f"A draw. Play again?"
        print("alexa: ", gm.alexa_hand.holding())
        print("player: ", gm.player_hand.holding())
        print("chips: ", gm.player_chips.total)
        return (
            handler_input.response_builder.speak(output)
            .set_should_end_session(False)
            .response
        )
    # if alexa higher than player, alexa wins, subtract bet, draw new cards
    # if draw then deal new cards


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.YesIntent"))
def yes(handler_input):
    if gm.game_state.state == "Playing":
        # clear hands
        gm.player_hand.clear_hand()
        gm.alexa_hand.clear_hand()
        # add new card to player, alexa, player , alexa
        cards.Hand.new_deal(gm.player_hand, gm.alexa_hand, gm.deck)
        p_hand = gm.player_hand.hand_held()
        a_hand = gm.alexa_hand.holding()
        print("alexa: ", gm.alexa_hand.holding())
        print("player: ", gm.player_hand.holding())
        output = f"""okay new round. I'll deal. You have {p_hand}.
            I have a {a_hand[1][1]} of {a_hand[1][0]} showing. how much would you like to bet?"""
        # handler_input.response_builder.add_directive(
        #     DelegateDirective(updated_intent=Intent(name='Betting')))
        return (
            handler_input.response_builder.speak(output)
            .set_should_end_session(False)
            .response
        )


handler = sb.lambda_handler()
