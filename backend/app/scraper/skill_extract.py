import re
from .skills import SKILL_PATTERNS

def extract_skills(text: str) -> list[str]:
    text = text.lower()
    found = []

    for skill, patterns in SKILL_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                found.append(skill)
                break

    return found