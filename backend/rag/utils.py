from pathlib import Path
from pypdf import PdfReader


def extract_text_from_file(file_path: Path) -> str:
    """Extract text from PDF or TXT file."""
    if file_path.suffix.lower() == ".pdf":
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text

    elif file_path.suffix.lower() == ".txt":
        return file_path.read_text(encoding="utf-8")

    return ""


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks