from py_ask_sdk_test.alexa_test import AlexaTest
from py_ask_sdk_test.classes import (
    TestItem as _TestItem,
    SkillSettings,
    SupportedInterfaces,
)
from py_ask_sdk_test.request_builders.launch_request_builder import LaunchRequestBuilder
from py_ask_sdk_test.request_builders.intent_request_builder import IntentRequestBuilder
from lambda2.code.lambda_function import handler
from lambda2.code.alexa import data, cards
from tests import speach_for_tests
from tests.test_config import skill_settings
import pytest

#   # interfaces your skill supports (audio, video etc.)


def test_launch_request():
    """Tests the LaunchRequest's speech and repromt output"""
    alexa_test = AlexaTest(handler)
    alexa_test.test(
        [
            _TestItem(
                LaunchRequestBuilder(skill_settings).build(),
                # expected_speech="Welcome to Simple 21. I've shuffled the cards. Say 'Ready' if you want to start or say "
                # "'Explain' to learn about this great game",
                expected_speech=(speach_for_tests.WELCOME, True),
                expected_repromt="Welcome to Simple 21. I've shuffled the cards. Say 'Ready' if you want to start or say "
                "'Explain' to learn about this great game",
                check_question=False,
            )
        ]
    )


@pytest.mark.xfail(raises=AssertionError)
def test_session_ready_game_speach():
    """Tests the SessionAttributeValidator"""
    alexa_test = AlexaTest(handler)
    alexa_test.test(
        [
            _TestItem(
                IntentRequestBuilder("ReadyGame", skill_settings).build(),
                expected_speech=(
                    """Now we can start the game. I'll deal. You have Ace and a King.
    I have a Five showing. how much would you like to bet?""",
                    True,
                ),
                should_end_session=False,
                session_attributes={
                    "PLAYER": ["Ten of Spades", "Ace of Spades"],
                    "ALEXA": ["King of Diamonds", "Queen of Hearts"],
                },
                expected_attributes={"PLAYER": ["Ten of Spades", "Ace of Spades"]},
            )
        ]
    )


def test_session_attribute_validator():
    """Tests the SessionAttributeValidator"""
    alexa_test = AlexaTest(handler)
    alexa_test.test(
        [
            _TestItem(
                IntentRequestBuilder("ReadyGame", skill_settings).build(),
                should_end_session=False,
                session_attributes={
                    "PLAYER": ["Ten of Spades", "Ace of Spades"],
                    "ALEXA": ["King of Diamonds", "Queen of Hearts"],
                },
                expected_attributes={"PLAYER": ["Ten of Spades", "Ace of Spades"]},
            )
        ]
    )


def test_session_attribute_Betting():
    """Tests the SessionAttributeValidator"""
    alexa_test = AlexaTest(handler)
    alexa_test.test(
        [
            _TestItem(
                IntentRequestBuilder("Betting", skill_settings)
                .with_slot("amount", 10)
                .build(),
                should_end_session=False,
                session_attributes={
                    "PLAYER": ["Ten of Spades", "Ace of Spades"],
                    "ALEXA": ["King of Diamonds", "Queen of Hearts"],
                },
                expected_speech=speach_for_tests.BETTING
                # expected_speech=f"""Okay you bet 10. You have Ten of Spades and a Ace of Spades. I have a Queen of Hearts showing. What you like to  Hit or Stand?""",
            )
        ]
    )


# @pytest.mark.skip("needs reworking")
def test_hit_intent():

    alexa_test = AlexaTest(handler)
    alexa_test.test(
        [
            _TestItem(
                IntentRequestBuilder("Hit", skill_settings)
                .with_slot("amount", 10)
                .build(),
                check_question=False,
                should_end_session=False,
                session_attributes={
                    "PLAYER": ["Ten of Spades"],
                    "ALEXA": ["King of Diamonds", "Queen of Hearts"],
                },
                expected_speech=(r"You.+", True)
                # expected_speech=f"""Okay you bet 10. You have Ten of
                # Spades and a Ace of Spades. I have a Queen of Hearts
                # showing. What you like to  Hit or Stand?""",
            )
        ]
    )
