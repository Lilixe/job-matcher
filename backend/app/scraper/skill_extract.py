import re
from .skills import SKILL_PATTERNS


def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"<[^>]+>", " ", text)         # remove HTML tags
    text = re.sub(r"[\n\r\t]", " ", text)        # remove newlines/tabs
    text = re.sub(r"\s+", " ", text)             # collapse spaces

    return text.strip()


def flatten_text(value) -> str:
    if value is None:
        return ""

    if isinstance(value, str):
        return value

    if isinstance(value, dict):
        return " ".join(str(v) for v in value.values() if v)

    if isinstance(value, list):
        return " ".join(str(v) for v in value if v)

    return str(value)


def extract_skills(text) -> list[str]:
    text = flatten_text(text)
    text = normalize_text(text)

    found = set()

    for skill, patterns in SKILL_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                found.add(skill)
                break

    return sorted(found)