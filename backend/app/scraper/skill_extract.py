import re
from .skills import SKILL_PATTERNS


def normalize_text(text: str) -> str:
    """
    Normalize and clean text for skill extraction.
    
    Performs multiple text cleaning operations including converting to lowercase,
    removing HTML tags, newlines, tabs, and collapsing multiple spaces into single spaces.
    
    Args:
        text (str): Raw text to normalize.
    
    Returns:
        str: Cleaned and normalized text in lowercase with extra whitespace removed.
    
    Example:
        >>> normalize_text("<p>Python & Java\\n\\n  Skills</p>")
        "python & java skills"
    """
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"<[^>]+>", " ", text)         # remove HTML tags
    text = re.sub(r"[\n\r\t]", " ", text)        # remove newlines/tabs
    text = re.sub(r"\s+", " ", text)             # collapse spaces

    return text.strip()


def flatten_text(value) -> str:
    """
    Convert various data types to a single flattened string.
    
    Handles multiple input types (string, dict, list) and recursively extracts
    text content. Useful for processing job descriptions that may be structured
    as mixed types in API responses.
    
    Args:
        value: Input data which can be str, dict, list, or any type.
    
    Returns:
        str: Flattened text representation. Returns empty string if input is None.
    
    Example:
        >>> flatten_text({"title": "Backend Dev", "desc": "Python expert"})
        "Backend Dev Python expert"
        
        >>> flatten_text(["Python", "FastAPI", None, "SQL"])
        "Python FastAPI SQL"
    """
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
    """
    Extract and identify skills from text using pattern matching.
    
    Flattens and normalizes input text, then matches against predefined skill patterns
    from the SKILL_PATTERNS dictionary. Returns all matched skills in sorted order.
    
    Args:
        text: Input text (string, dict, list, or other type) containing skill mentions.
    
    Returns:
        list[str]: Sorted list of identified skills. Returns empty list if no skills found.
    
    Example:
        >>> extract_skills("We need Python, FastAPI, and PostgreSQL expertise")
        ["fastapi", "postgresql", "python"]
        
        >>> extract_skills({"requirements": "Java and C++ programming"})
        ["c++", "java"]
    """
    text = flatten_text(text)
    text = normalize_text(text)

    found = set()

    for skill, patterns in SKILL_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                found.add(skill)
                break

    return sorted(found)