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

# Skill builder object

sb = CustomSkillBuilder(api_client=DefaultApiClient())

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# request handlers launch bstython with bstpy lambda2.py.lambda_function.handler

# start game
player_hand, alexa_hand, deck = cards.Hand().create_initial_hand()


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch.
     """
    # type: (HandlerInput) -> Response
    # set up deck and initial hand
    player_chips = 100

    speech_text = data.WELCOME
    # Set session attributes for the game
    game_session_attr = handler_input.attributes_manager.session_attributes
    if not game_session_attr:
        game_session_attr["GAME_STATE"] = 0
        game_session_attr["CHIPS"] = player_chips
        game_session_attr["ALEXA"] = alexa_hand.holding()
        game_session_attr["PLAYER"] = player_hand.holding()
        game_session_attr["last_speech"] = speech_text
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

    p_hand = player_hand.hand_held()
    a_hand = alexa_hand.hand_held()
    output = f"""Now we can start the game. I'll deal. You have {p_hand}.
    I have a {a_hand[1]} showing. how much would you like to bet?"""
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
    # current_intent gets details about returned intent for checking use .name
    # .slots etc
    game_session_attr = handler_input.attributes_manager.session_attributes
    slots = handler_input.request_envelope.request.intent.slots

    bet = slots["amount"].value

    game_session_attr["GAME_STATE"] = "RUNNING"
    # player_hand = game_session_attr["PLAYER"]
    alexa_hand = game_session_attr["ALEXA"]

    output = f"""Okay you bet {bet}. You have {player_hand[0]} and a {player_hand[1]}. I have a {alexa_hand[1]} showing. What you like to  Hit or Stand?"""

    return (
        handler_input.response_builder.speak(output)
        .set_should_end_session(False)
        .response
    )


@sb.request_handler(can_handle_func=is_intent_name("Hit"))
def play_handler(handler_input):
    game_session_attr = handler_input.attributes_manager.session_attributes
    print(player_hand.holding())

    # add card to player hand
    player_hand.hit(deck)
    print(player_hand.holding())
    # check if bust
    if not game_functions.isbust(player_hand):
        current_hand = player_hand.hand_held()
        output = f""" You have {current_hand}"""
        return (
            handler_input.response_builder.speak(output)
            .set_should_end_session(False)
            .response
        )
    else:
        output = "bust"
        return (
            handler_input.response_builder.speak(output)
            .set_should_end_session(False)
            .response
        )
    # ask hit or stand. if stand deal cards to alexa


# stand which lets alexa deal till higher than 17
@sb.request_handler(can_handle_func=is_intent_name("Stand"))
def stand_handler(handler_input):
    request_id_holder = handler_input.request_envelope.request.request_id
    directive_header = Header(request_id=request_id_holder)

    print(alexa_hand.value)
    while alexa_hand.value < 17:
        alexa_hand.hit(deck)
        current_hand = alexa_hand.hand_held()

        output = f""" I have {current_hand}"""
        speech = SpeakDirective(speech=output)
        directive_request = SendDirectiveRequest(
            header=directive_header, directive=speech
        )
        directive_service_client = (
            handler_input.service_client_factory.get_directive_service()
        )
        directive_service_client.enqueue(directive_request)

        print(output)
    bust = "Bust"
    handler_input.response_builder.speak(bust)

    return handler_input.response_builder.set_should_end_session(False).response


handler = sb.lambda_handler()
