"""Albert API type definitions.

All Pydantic models for Albert API responses are defined here.
"""

from albert.types.collections import (
    Collection,
    CollectionList,
    CollectionVisibility,
    Document,
    DocumentList,
    DocumentResponse,
)
from albert.types.search import (
    CarbonFootprintUsage,
    CarbonFootprintUsageKgCO2eq,
    CarbonFootprintUsageKWh,
    Chunk,
    ChunkList,
    Rerank,
    RerankResponse,
    RerankResult,
    SearchMethod,
    SearchResponse,
    SearchResult,
    Usage,
)
from albert.types.tools import (
    FileResponse,
    FileUploadResponse,
    MetricsUsage,
    OCRImageObject,
    OCRPageDimensions,
    OCRPageObject,
    OCRResponse,
    OCRUsage,
    ParsedDocument,
    ParsedDocumentMetadata,
    ParsedDocumentPage,
    UsageDetail,
    UsageList,
    UsageRecord,
)

__all__ = [
    # Collections
    "Collection",
    "CollectionList",
    "CollectionVisibility",
    "Document",
    "DocumentList",
    "DocumentResponse",
    # Search
    "CarbonFootprintUsage",
    "CarbonFootprintUsageKgCO2eq",
    "CarbonFootprintUsageKWh",
    "Chunk",
    "ChunkList",
    "Rerank",
    "RerankResponse",
    "RerankResult",
    "SearchMethod",
    "SearchResponse",
    "SearchResult",
    "Usage",
    # Tools / OCR / Parse / Files
    "FileResponse",
    "FileUploadResponse",
    "MetricsUsage",
    "OCRImageObject",
    "OCRPageDimensions",
    "OCRPageObject",
    "OCRResponse",
    "OCRUsage",
    "ParsedDocument",
    "ParsedDocumentMetadata",
    "ParsedDocumentPage",
    "UsageDetail",
    "UsageList",
    "UsageRecord",
]
