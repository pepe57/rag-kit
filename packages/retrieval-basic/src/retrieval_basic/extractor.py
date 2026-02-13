"""PDF text extraction module.

Re-exports from rag_core.pdf for backward compatibility.
The actual implementation lives in rag-core as a shared utility.
"""

from rag_core.pdf import extract_text_from_bytes, extract_text_from_pdf

__all__ = ["extract_text_from_bytes", "extract_text_from_pdf"]
