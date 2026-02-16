"""Types for Albert API Collections and Documents."""

from __future__ import annotations

from typing import Literal

from albert._models import BaseModel

# Enums as Literal types
CollectionVisibility = Literal["private", "public"]


class Collection(BaseModel):
    """A collection in Albert API.

    The ``POST /collections`` endpoint returns only ``{"id": ...}``,
    so all fields except ``id`` are optional.  Full metadata is
    returned by ``GET /collections`` and ``GET /collections/{id}``.
    """

    object: str = "collection"
    id: int
    name: str | None = None
    owner: str | None = None
    description: str | None = None
    visibility: CollectionVisibility | None = None
    created: int | None = None
    updated: int | None = None
    documents: int = 0


class CollectionList(BaseModel):
    """List of collections (Searches response wrapper)."""

    object: str = "list"
    data: list[Collection] = []


class Document(BaseModel):
    """A document in a collection."""

    object: str = "document"
    id: int
    name: str
    collection_id: int
    created: int
    chunks: int | None = None


class DocumentResponse(BaseModel):
    """Response from creating a document (just the ID)."""

    id: int


class DocumentList(BaseModel):
    """List of documents."""

    object: str = "list"
    data: list[Document] = []
