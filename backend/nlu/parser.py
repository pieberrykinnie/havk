"""Lightweight intent parser for SMS/WhatsApp bot.

Loads regex patterns from `intents.yml` and matches incoming text.
If no pattern matches, returns intent="unknown".
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional

import yaml

# Load patterns once at import time
_INTENTS_PATH = Path(__file__).with_suffix(".yml")

with _INTENTS_PATH.open("r", encoding="utf-8") as fp:
    _RAW_PATTERNS: Dict[str, List[str]] = yaml.safe_load(fp)

_PATTERNS: Dict[str, List[re.Pattern[str]]] = {
    intent: [re.compile(pat, re.IGNORECASE) for pat in pats]
    for intent, pats in _RAW_PATTERNS.items()
}

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
    for intent, patterns in _PATTERNS.items():
        if any(p.search(message) for p in patterns):
            return intent
    return "unknown"


def list_intents() -> List[str]:
    """Return available intent names."""
    return list(_PATTERNS.keys())