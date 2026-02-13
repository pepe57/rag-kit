"""Document parsing via Albert's parse API.

Provides the same interface as retrieval-basic (process_pdf_file,
format_as_context, extract_text_from_bytes) so the two packages
are interchangeable in context_loader.py / modules.yml.

The key difference: retrieval-basic only handles PDFs via local pypdf,
while this module uses Albert's server-side parse API which supports
many document formats with high-quality OCR and markdown conversion.
"""

from __future__ import annotations

import logging
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from albert import AlbertClient


logger = logging.getLogger(__name__)


# File types supported by Albert's parse API (/parse-beta).
# context_loader reads this to know which extensions to route here.
SUPPORTED_EXTENSIONS: list[str] = [
    ".pdf",
    ".docx",
    ".doc",
    ".pptx",
    ".ppt",
    ".xlsx",
    ".xls",
    ".odt",
    ".ods",
    ".odp",
    ".html",
    ".htm",
    ".md",
    ".txt",
    ".csv",
    ".rtf",
    ".epub",
]


def _get_client() -> AlbertClient:
    """Create an AlbertClient from environment variables."""
    from albert import AlbertClient

    return AlbertClient()


def _parse_and_combine(
    client: AlbertClient,
    file_path: Path,
    force_ocr: bool = False,
) -> str:
    """Parse a file via Albert API and combine page contents."""
    parsed = client.parse(file_path=file_path, force_ocr=force_ocr)

    text_parts: list[str] = []
    for page in parsed.data:
        if page.content:
            text_parts.append(page.content)

    return "\n".join(text_parts)


# --- Generic (multi-format) API ---


def extract_text(
    path: str | Path,
    *,
    client: AlbertClient | None = None,
    force_ocr: bool = False,
) -> str:
    """Extract text from a document using Albert's parse API.

    Supports all formats in SUPPORTED_EXTENSIONS (PDF, DOCX, PPTX, etc.).

    Args:
        path: Path to the document file.
        client: Optional pre-configured Albert client.
        force_ocr: Force OCR on all pages (default: False).

    Returns:
        Extracted text content as markdown.

    Raises:
        FileNotFoundError: If the file doesn't exist.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    client = client or _get_client()
    return _parse_and_combine(client, path, force_ocr=force_ocr)


def extract_text_from_bytes(
    data: bytes,
    *,
    suffix: str = ".pdf",
    client: AlbertClient | None = None,
    force_ocr: bool = False,
) -> str:
    """Extract text from file bytes using Albert's parse API.

    Args:
        data: Raw file content as bytes.
        suffix: File extension hint for the temp file (e.g. ".pdf", ".docx").
        client: Optional pre-configured Albert client.
        force_ocr: Force OCR on all pages.

    Returns:
        Extracted text content as markdown.
    """
    client = client or _get_client()

    # Write bytes to a temp file (Albert parse API requires a file path)
    with NamedTemporaryFile(suffix=suffix, delete=True) as tmp:
        tmp.write(data)
        tmp.flush()
        return _parse_and_combine(client, Path(tmp.name), force_ocr=force_ocr)


def format_as_context(text: str, filename: str) -> str:
    """Format extracted text with delimiters for context injection.

    Same format as retrieval-basic for interchangeability.

    Args:
        text: The extracted text content.
        filename: The name of the source file (for labeling).

    Returns:
        Formatted text with file delimiters.
    """
    return (
        f"\n\n--- Content of attached file '{filename}' ---\n"
        f"{text}\n"
        f"--- End of file ---\n"
    )


def process_file(
    path: str | Path,
    filename: str | None = None,
    *,
    client: AlbertClient | None = None,
) -> str:
    """Parse any supported document and format it for context injection.

    This is the primary entry point for context_loader. Supports all
    file types in SUPPORTED_EXTENSIONS.

    Args:
        path: Path to the document file.
        filename: Optional display name for the file.
        client: Optional pre-configured Albert client.

    Returns:
        Formatted text ready for context injection.
    """
    path = Path(path)
    display_name = filename if filename else path.name

    text = extract_text(path, client=client)
    return format_as_context(text, display_name)


def process_multiple_files(
    paths: list[str | Path],
    *,
    client: AlbertClient | None = None,
) -> str:
    """Process multiple document files and combine their context.

    Args:
        paths: List of paths to document files.
        client: Optional pre-configured Albert client.

    Returns:
        Combined formatted text from all files.
    """
    client = client or _get_client()
    results: list[str] = []

    for path in paths:
        try:
            formatted = process_file(path, client=client)
            results.append(formatted)
        except Exception as e:
            path_obj = Path(path)
            results.append(f"\n\nError reading '{path_obj.name}': {e!s}\n")

    return "".join(results)


# --- Backward-compatible aliases (match retrieval-basic interface) ---


def extract_text_from_pdf(
    path: str | Path,
    *,
    client: AlbertClient | None = None,
    force_ocr: bool = False,
) -> str:
    """Extract text from a PDF file. Alias for extract_text()."""
    return extract_text(path, client=client, force_ocr=force_ocr)


def process_pdf_file(
    path: str | Path,
    filename: str | None = None,
    *,
    client: AlbertClient | None = None,
) -> str:
    """Process a PDF file. Alias for process_file()."""
    return process_file(path, filename=filename, client=client)
