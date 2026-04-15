import io
from pypdf import PdfReader


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract all text content from a PDF file.
    
    Reads a PDF file from bytes, iterates through all pages, and extracts text content
    from each page. Useful for parsing resume PDFs to prepare text for skill extraction.
    
    Args:
        file_bytes (bytes): PDF file content as bytes (typically from an uploaded file).
    
    Returns:
        str: Concatenated text from all pages separated by newlines. Returns empty string if no text found.
    
    Raises:
        pypdf.errors.PdfReadError: If the bytes do not represent a valid PDF.
    
    Example:
        >>> with open("resume.pdf", "rb") as f:
        ...     content = extract_text_from_pdf(f.read())
        >>> print(content[:100])
        "John Doe\\nExperienced Software Engineer with 5 years of Python development..."
    """
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()