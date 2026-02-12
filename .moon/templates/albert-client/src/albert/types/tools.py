"""Types for Albert API Tools, OCR, Parse, Files, and Usage endpoints."""

from __future__ import annotations

from albert._models import BaseModel
from albert.types.search import CarbonFootprintUsage, Usage


# --- OCR Types ---


class OCRPageDimensions(BaseModel):
    """Dimensions of a PDF page screenshot image."""

    dpi: int
    height: int
    width: int


class OCRImageObject(BaseModel):
    """An extracted image from an OCR page."""

    id: str
    image_base64: str | None = None
    image_annotation: str | None = None
    top_left_x: int | None = None
    top_left_y: int | None = None
    bottom_right_x: int | None = None
    bottom_right_y: int | None = None


class OCRPageObject(BaseModel):
    """OCR result for a single page."""

    index: int
    images: list[OCRImageObject] = []
    markdown: str | None = None
    dimensions: OCRPageDimensions | None = None


class OCRUsage(BaseModel):
    """OCR-specific usage information."""

    pages_processed: int
    doc_size_bytes: int | None = None


class OCRResponse(BaseModel):
    """Response from the OCR endpoint."""

    pages: list[OCRPageObject] = []
    document_annotation: str | None = None
    id: str | None = None
    model: str | None = None
    usage: Usage | None = None
    usage_info: OCRUsage | None = None


# --- Parse Types ---


class ParsedDocumentMetadata(BaseModel):
    """Metadata for a parsed document page."""

    document_name: str
    page: int = 0


class ParsedDocumentPage(BaseModel):
    """A single page from a parsed document."""

    object: str = "documentPage"
    content: str
    images: dict[str, str] = {}
    metadata: ParsedDocumentMetadata | None = None


class ParsedDocument(BaseModel):
    """Response from the parse endpoint."""

    object: str = "list"
    data: list[ParsedDocumentPage] = []
    usage: Usage | None = None


# --- File Types ---


class FileResponse(BaseModel):
    """Response from the (deprecated) file upload endpoint."""

    id: int


# --- Usage Types (Me/Usage endpoint) ---


class CarbonFootprintUsageDetail(BaseModel):
    """Carbon footprint detail for usage records (nullable fields)."""

    kWh: CarbonFootprintUsageKWhDetail | None = None
    kgCO2eq: CarbonFootprintUsageKgCO2eqDetail | None = None


class CarbonFootprintUsageKWhDetail(BaseModel):
    """Carbon footprint in kWh (nullable variant for usage detail)."""

    min: float | None = None
    max: float | None = None


class CarbonFootprintUsageKgCO2eqDetail(BaseModel):
    """Carbon footprint in kgCO2eq (nullable variant for usage detail)."""

    min: float | None = None
    max: float | None = None


class MetricsUsage(BaseModel):
    """Metrics information in usage records."""

    latency: int | None = None
    ttft: int | None = None


class UsageDetail(BaseModel):
    """Detailed usage information for a single usage record."""

    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    cost: float | None = None
    carbon: CarbonFootprintUsage | None = None
    metrics: MetricsUsage | None = None


class UsageRecord(BaseModel):
    """A single usage record from the me/usage endpoint."""

    object: str = "me.usage"
    model: str | None = None
    key: str | None = None
    endpoint: str | None = None
    method: str | None = None
    status: int | None = None
    usage: UsageDetail | None = None
    created: int


class UsageList(BaseModel):
    """List of usage records."""

    object: str = "list"
    data: list[UsageRecord] = []


# Backward compatibility aliases
FileUploadResponse = FileResponse
