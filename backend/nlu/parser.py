"""Lightweight intent parser for SMS/WhatsApp bot.

Loads regex patterns from `intents.yml` and matches incoming text.
If no pattern matches, returns intent="unknown".
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

import unicodedata
from unidecode import unidecode

import yaml

# Load patterns once at import time
_INTENTS_PATH = Path(__file__).with_suffix(".yml")

with _INTENTS_PATH.open("r", encoding="utf-8") as fp:
    _RAW_PATTERNS: Dict[str, List[str]] = yaml.safe_load(fp)

_PATTERNS: Dict[str, List[re.Pattern[str]]] = {
    intent: [re.compile(pat, re.IGNORECASE) for pat in pats]
    for intent, pats in _RAW_PATTERNS.items()
}

def _normalise(text: str) -> str:
    """Return lower-case ASCII representation with accents removed.

    Uses `unidecode` for transliteration so that non-Latin scripts roughly map
    to ASCII phonetics (e.g. Devanagari → Latin).  This improves regex match
    consistency without changing the YAML patterns.
    """
    # First, Unicode NFC normalise to combine accents
    text_norm = unicodedata.normalize("NFC", text)
    # Transliterate to ASCII
    text_ascii = unidecode(text_norm)
    return text_ascii.lower()

def parse_message(message: str) -> str:
    """Return the first intent whose regex matches the message.

    Parameters
    ----------
    message : str
        Incoming text (user message).

    Returns
    -------
    str
        Intent name or "unknown" if none matched.
    """
    msg_norm = _normalise(message)

    for intent, patterns in _PATTERNS.items():
        if any(p.search(msg_norm) for p in patterns):
            return intent
    return "unknown"


def list_intents() -> List[str]:
    """Return available intent names."""
    return list(_PATTERNS.keys())