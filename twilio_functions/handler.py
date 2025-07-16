"""Twilio SMS Webhook Handler – IrrigaBot

This lightweight function mirrors what would run in Twilio Functions or as a /twilio
FastAPI route. It parses the incoming SMS body, detects intent via the NLU parser,
and returns an XML **TwiML** response.
"""
from __future__ import annotations

from typing import Dict
from xml.etree.ElementTree import Element, tostring

from backend.nlu.parser import parse_message


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_twiml(message: str) -> str:
    """Return TwiML string with single `<Message>` node."""

    root = Element("Response")
    node = Element("Message")
    node.text = message
    root.append(node)

    # tostring returns `bytes` by default; decode to `str` for convenience
    return tostring(root, encoding="unicode")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def handle_sms(event: Dict[str, str]) -> str:  # noqa: D401
    """Handle Twilio webhook.

    Parameters
    ----------
    event : dict
        Key-value map of request parameters (Twilio forwards form data). At
        minimum must contain the `Body` key.

    Returns
    -------
    str
        TwiML XML string to send back to the requester.
    """
    body = event.get("Body", "")
    intent = parse_message(body)

    if intent == "join":
        response_text = (
            "Welcome to IrrigaBot! We'll send irrigation advice daily. "
            'Reply "done" after irrigating to improve suggestions.'
        )
    elif intent == "done":
        response_text = "Great! Your feedback has been recorded. 👍"
    elif intent == "leave":
        response_text = "You have been unsubscribed. Bye!"
    else:
        response_text = (
            'Sorry, I did not understand. Type "join" to enrol or "leave" to quit.'
        )

    return _build_twiml(response_text)