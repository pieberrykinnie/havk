import json
import re
import sys
from pathlib import Path
from typing import List, Optional


# --------------------------
# Helper extraction routines
# --------------------------

def _extract(pattern: str, text: str, *, flags: int = re.IGNORECASE, fallback: Optional[str] = None) -> Optional[str]:
    """Return the first capture group for *pattern* or *fallback* if not found."""
    match = re.search(pattern, text, flags)
    if match:
        return match.group(1).strip()
    return fallback


def _extract_all(pattern: str, text: str, *, flags: int = re.IGNORECASE, max_matches: int = 0) -> List[str]:
    """Return **all** capture group 1 occurrences for *pattern*.

    If *max_matches* > 0, truncate to that many items.
    """
    matches = [m.group(1).strip() for m in re.finditer(pattern, text, flags)]
    if max_matches > 0:
        matches = matches[:max_matches]
    return matches


# -------------------------------------
# Primary parsing function as specified
# -------------------------------------

def parse_devpost(content: str) -> str:
    """Parse raw Devpost page content.

    The output string follows the specification from the AUTOMATIC CONTEXT
    EXTRACTION protocol.
    """
    # 1. Theme (fallback to "innovation")
    theme = _extract(r"Theme[: ]*([^\n<]+)", content, fallback="innovation")

    # 2. Judging criteria – capture bullet/line headings under "Judging Criteria"
    criteria_block = _extract(r"Judging Criteria(.*?)(?:You're registered|Questions\?)", content, flags=re.IGNORECASE | re.S)
    criteria: List[str] = []
    if criteria_block:
        criteria = _extract_all(r"^([A-Za-z ][A-Za-z]+)\n", criteria_block, flags=re.MULTILINE)

    # Fallback if nothing captured
    if not criteria:
        criteria = ["Technical Depth", "Creativity", "Usability"]

    # 3. Deadlines – try multiple patterns (MM/DD or `Jul 18, 2025`)
    deadlines = _extract_all(r"(\w{3,9}\s\d{1,2},\s\d{4})", content)
    if not deadlines:
        # Try numeric formats like 7/18/25
        deadlines = _extract_all(r"\b(\d{1,2}/\d{1,2}/\d{2,4})\b", content)

    # 4. Prize amounts (monetary or fallback description)
    prizes = _extract_all(r"\$[\d,]+(?:\.\d+)?", content, max_matches=3)
    if not prizes:
        # Look for non-cash description lines after "Prizes" header
        noncash_block = _extract(r"Prizes(.*?)(?:Devpost Achievements|Judges)", content, flags=re.IGNORECASE | re.S)
        if noncash_block:
            prizes = _extract_all(r"^(?:\d+\w* Place.*?)$", noncash_block, flags=re.MULTILINE)
        if not prizes:
            prizes = ["non-cash"]

    # Compose summary string
    summary = (
        f"Building for '{theme}' | Prizes: {', '.join(prizes)} | "
        f"Deadline: {deadlines[0] if deadlines else '48h'} | "
        f"Criteria: {', '.join(criteria[:5])}"
    )
    return summary


# --------------------------
# Simple CLI for convenience
# --------------------------

def main() -> None:
    """Read JSON containing `devpost_page` and print the parsed summary."""
    if len(sys.argv) > 1 and Path(sys.argv[1]).exists():
        input_json = json.loads(Path(sys.argv[1]).read_text())
    else:
        try:
            input_json = json.load(sys.stdin)
        except json.JSONDecodeError as exc:
            sys.exit(f"[ERROR] Expected JSON on stdin: {exc}")

    page_content = input_json.get("devpost_page", "")
    if not page_content:
        sys.exit("[ERROR] Key 'devpost_page' missing or empty in input JSON.")

    summary = parse_devpost(page_content)
    print(summary)


if __name__ == "__main__":
    main()