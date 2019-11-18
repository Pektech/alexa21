import json
import logging

from ask_sdk_core.skill_builder import SkillBuilder
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

from .alexa import data, cards

# Skill builder object

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# request handlers launch bstython with bstpy lambda2.py.lambda_function.handler

# start game


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch.
     """
    # type: (HandlerInput) -> Response
    # set up deck and initial hand
    player_chips = cards.Chips()
    deck = cards.Deck()
    deck.shuffle()
    alexa_hand = cards.Hand()
    player_hand = cards.Hand()
    player_hand.add_cards(deck.deal())
    alexa_hand.add_cards(deck.deal())
    player_hand.add_cards(deck.deal())
    alexa_hand.add_cards(deck.deal())

    speech_text = data.WELCOME
    # Set session attributes for the game
    game_session_attr = handler_input.attributes_manager.session_attributes
    if not game_session_attr:
        game_session_attr["GAME_STATE"] = 0
        game_session_attr["CHIPS"] = player_chips.total
        game_session_attr["ALEXA"] = alexa_hand.holding()
        game_session_attr["PLAYER"] = player_hand.holding()
        game_session_attr["last_speech"] = speech_text
    return (
        handler_input.response_builder.speak(speech_text)
        .set_card(SimpleCard("Simple 21", speech_text))
        .set_should_end_session(False)
        .response
    )


@sb.request_handler(can_handle_func=lambda handler_input: is_intent_name("ReadyGame"))
def start_game(handler_input):
    game_session_attr = handler_input.attributes_manager.session_attributes
    game_session_attr["GAME_STATE"] = "RUNNING"
    player_hand = game_session_attr["PLAYER"]
    alexa_hand = game_session_attr["ALEXA"]
    output = f"""Now we can start the game. I'll deal. You have {player_hand[0]} and a {player_hand[1]}.
    I have a {alexa_hand[1]} showing. how much would you like to bet"""
    # handler_input.response_builder.add_directive(
    #     DelegateDirective(updated_intent=Intent(name='Betting')))
    return (
        handler_input.response_builder.speak(output)
        .set_should_end_session(False)
        .response
    )


# this intent handles the bet and has a required slot


@sb.request_handler(can_handle_func=lambda handler_input: is_intent_name("Betting"))
def bet_handler(handler_input):
    # handles that a bet has been set and remembers amount
    # current_intent gets details about returned intent for checking use .name,
    # .slots etc
    print("starting bet")
    current_intent = handler_input.request_envelope.request.intent
    game_session_attr = handler_input.attributes_manager.session_attributes
    logger.info("In BetHandler")
    output = f"current intent is {current_intent},  game session is {game_session_attr}"
    return handler_input.response_builder.speak(output).response


handler = sb.lambda_handler()
