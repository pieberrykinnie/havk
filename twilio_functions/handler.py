"""Twilio SMS & Voice Webhook Handler – IrrigaBot

Supports both SMS (text) and Voice (IVR) requests from Twilio.
For SMS, returns <Message> TwiML with text.
For Voice, returns <Say> TwiML for TTS (text-to-speech).
Intent detection is shared for both channels.
"""
from __future__ import annotations

from typing import Dict
from xml.etree.ElementTree import Element, tostring

from backend.nlu.parser import parse_message


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_twiml(message: str, voice: bool = False) -> str:
    """Return TwiML string with single <Message> or <Say> node."""
    root = Element("Response")
    if voice:
        node = Element("Say")
        node.text = message
        node.set("voice", "Polly.Joanna")  # Use a clear TTS voice
    else:
        node = Element("Message")
        node.text = message
    root.append(node)
    return tostring(root, encoding="unicode")


def _badge_for_area(area: float) -> str:
    if area >= 4000:
        return "🏆 Gold"
    elif area >= 2000:
        return "🥈 Silver"
    elif area >= 1000:
        return "🥉 Bronze"
    return "🌱 Seedling"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def handle_sms(event: Dict[str, str]) -> str:  # noqa: D401
    """Handle Twilio webhook (SMS or Voice).

    Parameters
    ----------
    event : dict
        Key-value map of request parameters (Twilio forwards form data). At
        minimum must contain the `Body` key. If `CallSid` is present, treat as voice.

    Returns
    -------
    str
        TwiML XML string to send back to the requester.
    """
    body = event.get("Body", "")
    is_voice = "CallSid" in event or event.get("ChannelToAddress") == "voice"
    intent = parse_message(body)

    if intent == "join":
        # Simulate lookup of area for badge (in real use, fetch from API)
        area = 2500  # Placeholder; in prod, fetch from /farmers or /stats
        badge = _badge_for_area(area)
        response_text = (
            f"Welcome to IrrigaBot! Your badge: {badge}. "
            "We'll send irrigation advice daily. "
            'Reply "done" after irrigating to improve suggestions.'
        )
    elif intent == "done":
        response_text = "Great! Your feedback has been recorded."
    elif intent == "leave":
        response_text = "You have been unsubscribed. Bye!"
    else:
        response_text = (
            'Sorry, I did not understand. Say "join" to enrol or "leave" to quit.'
        )

    return _build_twiml(response_text, voice=is_voice)