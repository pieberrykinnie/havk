import json
import re
import sys
from pathlib import Path
from typing import List, Optional, Dict
from dataclasses import dataclass


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


# -------------------------------------------------------
# Structured extractor (reuses the regex helpers above)
# -------------------------------------------------------

@dataclass
class DevpostInfo:
    """Structured representation of the critical elements we parse from a Devpost page."""

    theme: str
    criteria: List[str]
    deadlines: List[str]
    prizes: List[str]


def extract_devpost_info(content: str) -> DevpostInfo:  # noqa: C901 – keep simple for now
    """Return a **structured** representation of the Devpost page.

    This is a superset of the data used by `parse_devpost`, enabling richer
    downstream automation like intelligent context bootstrapping.
    """
    # Theme
    theme = _extract(r"Theme[: ]*([^\n<]+)", content, fallback="innovation")

    # Criteria block extraction
    criteria_block = _extract(
        r"Judging Criteria(.*?)(?:You're registered|Questions\?)",
        content,
        flags=re.IGNORECASE | re.S,
    )
    criteria: List[str] = []
    if criteria_block:
        criteria = _extract_all(r"^([A-Za-z ][A-Za-z]+)\n", criteria_block, flags=re.MULTILINE)
    if not criteria:
        criteria = ["Technical Depth", "Creativity", "Usability"]

    # Deadlines – natural language and numeric formats
    deadlines = _extract_all(r"(\w{3,9}\s\d{1,2},\s\d{4})", content)
    if not deadlines:
        deadlines = _extract_all(r"\b(\d{1,2}/\d{1,2}/\d{2,4})\b", content)

    # Prizes – monetary first, fall back to textual
    prizes = _extract_all(r"\$[\d,]+(?:\.\d+)?", content, max_matches=3)
    if not prizes:
        noncash_block = _extract(r"Prizes(.*?)(?:Devpost Achievements|Judges)", content, flags=re.IGNORECASE | re.S)
        if noncash_block:
            prizes = _extract_all(r"^(?:\d+\w* Place.*?)$", noncash_block, flags=re.MULTILINE)
        if not prizes:
            prizes = ["non-cash"]

    return DevpostInfo(theme=theme, criteria=criteria, deadlines=deadlines, prizes=prizes)


# -------------------------------------------------------
# Intelligent Context Bootstrapping utilities
# -------------------------------------------------------

def select_tech_stack(theme: str) -> str:
    """Choose an appropriate tech stack based on the theme keywords."""
    theme_lower = theme.lower()

    # Primary decision branches
    if re.search(r"\bweb\b|online|website|portal", theme_lower):
        return "Next.js/FastAPI"
    if re.search(r"\bmobile\b|android|ios|app", theme_lower):
        return "Flutter/Firebase"
    if re.search(r"\b(ai|ml|machine learning|deep learning)\b", theme_lower):
        return "Python + PyTorch + FastAPI"
    if re.search(r"metaverse|vr|ar|xr", theme_lower):
        return "Unity/C#"

    # Default fallback
    return "Next.js/FastAPI"


def generate_wow_factor(theme: str) -> str:
    """Generate a wow-factor idea snippet to spice up the project."""
    theme_lower = theme.lower()

    if "metaverse" in theme_lower or re.search(r"\b(ar|vr|xr)\b", theme_lower):
        return "AR component"
    if re.search(r"\b(ai|ml|machine learning)\b", theme_lower):
        return "Generative AI feature"

    # Catch-all fallback
    return "real-time AI animation"


def calculate_judging_weights(criteria: List[str]) -> Dict[str, float]:
    """Return a normalized weight mapping keyed by criterion names.

    Heuristic: if any criterion contains "technical" we boost it to 0.4 and
    distribute the remaining 0.6 evenly. Otherwise use equal distribution but
    expose an explicit `Innovation` weight of 0.25 (remaining evenly split).
    """
    if not criteria:
        return {}

    criteria_lower = [c.lower() for c in criteria]
    total_criteria = len(criteria)

    weights: Dict[str, float] = {}

    # Case 1: Special boost for Technical-style criterion
    tech_indices = [i for i, c in enumerate(criteria_lower) if "technical" in c]
    if tech_indices:
        boosted_share = 0.4
        remaining_share = 1.0 - boosted_share
        # Distribute remaining among non-tech
        others_count = total_criteria - len(tech_indices)
        even_share = remaining_share / others_count if others_count else 0.0
        for i, name in enumerate(criteria):
            if i in tech_indices:
                weights[name] = boosted_share / len(tech_indices)
            else:
                weights[name] = round(even_share, 3)
        return weights

    # Case 2: No explicit technical criterion – equal distribution, but expose innovation
    even_share = round(1.0 / total_criteria, 3)
    for name in criteria:
        weights[name] = even_share

    # Add an explicit innovation_weight entry per spec
    weights["Innovation"] = 0.25
    return weights


def bootstrap_context(devpost_content: str) -> Dict[str, object]:
    """High-level helper that fuses parsing + intelligent bootstrap steps."""
    info = extract_devpost_info(devpost_content)

    tech_stack = select_tech_stack(info.theme)
    wow_factor = generate_wow_factor(info.theme)
    weights = calculate_judging_weights(info.criteria)

    return {
        "theme": info.theme,
        "criteria": info.criteria,
        "deadline": info.deadlines[0] if info.deadlines else "48h",
        "prizes": info.prizes,
        "tech_stack": tech_stack,
        "wow_factor": wow_factor,
        "weights": weights,
    }


# -------------------------------------------------------
# Export CLI for bootstrap as sub-command (optional)
# -------------------------------------------------------

def _cli_bootstrap(devpost_json_path: Path) -> None:
    """Print a JSON dictionary with the bootstrapped context."""
    data = json.loads(devpost_json_path.read_text())
    page = data.get("devpost_page", "")
    ctx = bootstrap_context(page)
    print(json.dumps(ctx, indent=2))


# Amend main() to accept --bootstrap flag without breaking existing usage
_original_main = main  # type: ignore


def main() -> None:  # noqa: PLR0912 – compact branching for CLI args
    if "--bootstrap" in sys.argv:
        try:
            path_idx = sys.argv.index("--bootstrap") + 1
            target_path = Path(sys.argv[path_idx])
        except Exception:
            sys.exit("Usage: python devpost_parser.py --bootstrap <input.json>")
        if not target_path.exists():
            sys.exit(f"[ERROR] File does not exist: {target_path}")
        _cli_bootstrap(target_path)
    else:
        _original_main()


# Only execute when run as script (preserving previous behavior)
if __name__ == "__main__":
    main()