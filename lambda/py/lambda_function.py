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


# Skill builder object

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch."""
    # type: (HandlerInput) -> Response
    speech_text = "Welcome to the Alexa Skills Kit, you can say hello!"

    return (
        handler_input.response_builder.speak(speech_text)
        .set_card(SimpleCard("Hello World", speech_text))
        .set_should_end_session(False)
        .response
    )


handler = sb.lambda_handler()
