from xml.etree import ElementTree as ET

from twilio_functions.handler import handle_sms


def _msg_text(twiml: str) -> str:
    root = ET.fromstring(twiml)
    return root.findtext("Message")


def test_join_flow():
    xml = handle_sms({"Body": "join"})
    assert "Welcome" in _msg_text(xml)


def test_unknown_flow():
    xml = handle_sms({"Body": "foobar"})
    assert "did not understand" in _msg_text(xml)


def test_voice_join_flow():
    xml = handle_sms({"Body": "join", "CallSid": "CA123"})
    assert "<Say" in xml
    assert "Welcome" in _msg_text(xml)

def test_voice_unknown_flow():
    xml = handle_sms({"Body": "foobar", "CallSid": "CA456"})
    assert "<Say" in xml
    assert "did not understand" in _msg_text(xml)