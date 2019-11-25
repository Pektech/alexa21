from py_ask_sdk_test.alexa_test import AlexaTest
from py_ask_sdk_test.classes import (
    TestItem as _TestItem,
    SkillSettings,
    SupportedInterfaces,
)
from py_ask_sdk_test.request_builders.launch_request_builder import LaunchRequestBuilder
from py_ask_sdk_test.request_builders.intent_request_builder import IntentRequestBuilder
from lambda2.code.lambda_function import handler
import pytest

skill_settings = SkillSettings(
    app_id="amzn1.ask.skill.9843a71e-2057-40d6-bef2-65eba17b0978",
    user_id="amzn1.ask.account.AEZQ5YDE3DETH3VN36YBYR4GV5N7TWRCAB4C27SABIVJSDNISAU4KO2LNJBCFTBWHHPYR4GG776N36K42S74NODU5M7AXOKPS2NWHJ6GAEYNMI33HOO4BQ6V4W7P4SV5DWPHAAW3VFHAXSFQ3WU3A7OCXFP3MSZNRWYU6W7EIU5FFCSFUUR5TJKJ5SWY4AY3T6KUAGHOZWVJLRY",
    device_id="amzn1.ask.device.AFD3UB6HGHW7KGHUZMKIWHFDLIGMHIECBXNDUFTOXY3GAMGCGFHRPIWWCBGL5VUV3FSO2K6MTSZKKOMQML6GJMCNMFYXX7VFZTLIDD33VOW7PIGY2HJUBZF77QB5MRSROAH4ILVKWUFKPH35KVU72TAJE7JQ",
    locale="en-US",
    interfaces=SupportedInterfaces(),
)  # interfaces your skill supports (audio, video etc.)


def test_launch_request():
    """Tests the LaunchRequest's speech and repromt output"""
    alexa_test = AlexaTest(handler)
    alexa_test.test(
        [
            _TestItem(
                LaunchRequestBuilder(skill_settings).build(),
                expected_speech="Welcome to Simple 21. I've shuffled the cards. Say 'Ready' if you want to start or say "
                "'Explain' to learn about this great game",
                expected_repromt="Welcome to Simple 21. I've shuffled the cards. Say 'Ready' if you want to start or say "
                "'Explain' to learn about this great game",
                check_question=False,
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
                expected_attributes={"GAME_STATE": "RUNNING"},
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
                expected_speech=f"""Okay you bet 10. You have Ten of Spades and a Ace of Spades. I have a Queen of Hearts showing. What you like to  Hit or Stand?""",
            )
        ]
    )
