"""Types for Albert API Search and Rerank endpoints."""

from __future__ import annotations

from typing import Literal

from albert._models import BaseModel

# Search method types
SearchMethod = Literal["hybrid", "semantic", "lexical"]


# --- Usage (inline, used in search/rerank responses) ---


class CarbonFootprintUsageKWh(BaseModel):
    """Carbon footprint in kWh."""

    min: float = 0.0
    max: float = 0.0


class CarbonFootprintUsageKgCO2eq(BaseModel):
    """Carbon footprint in kgCO2eq."""

    min: float = 0.0
    max: float = 0.0


class CarbonFootprintUsage(BaseModel):
    """Carbon footprint usage."""

    kWh: CarbonFootprintUsageKWh | None = None
    kgCO2eq: CarbonFootprintUsageKgCO2eq | None = None


class Usage(BaseModel):
    """Inline usage information returned in API responses."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost: float = 0.0
    carbon: CarbonFootprintUsage | None = None
    requests: int = 0


# --- Chunks ---


class Chunk(BaseModel):
    """A chunk of a document."""

    object: str = "chunk"
    id: int
    collection_id: int
    document_id: int
    content: str
    metadata: dict | None = None
    created: int | None = None


class ChunkList(BaseModel):
    """List of chunks."""

    object: str = "list"
    data: list[Chunk] = []


# --- Search ---


class SearchResult(BaseModel):
    """A single search result with method, score, and chunk."""

    method: SearchMethod
    score: float
    chunk: Chunk


class SearchResponse(BaseModel):
    """Response from the search endpoint."""

    object: str = "list"
    data: list[SearchResult] = []
    usage: Usage | None = None


# --- Rerank ---


class Rerank(BaseModel):
    """Deprecated rerank result format (in `data` field)."""

    object: str = "rerank"
    score: float
    index: int


class RerankResult(BaseModel):
    """A single rerank result with relevance score and original index."""

    relevance_score: float
    index: int


class RerankResponse(BaseModel):
    """Response from the rerank endpoint."""

    object: str = "list"
    id: str
    data: list[Rerank] = []
    results: list[RerankResult] = []
    model: str
    usage: Usage | None = None
