import pytest

from lambda2.code.alexa.speech_functions import build_hand


def test_build_hand():

    expected_speech = "Now we can start the game. I'll deal. You have an Ace of Hearts and a Four of Diamonds. I have a Ten of Hearts showing. How much would you like to bet?"

    built_speech = build_hand()

    assert expected_speech == built_speech
