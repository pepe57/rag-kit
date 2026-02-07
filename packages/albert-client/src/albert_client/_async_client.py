"""Async Albert Client implementation."""

import os

from openai import AsyncOpenAI


class AsyncAlbertClient:
    """Async version of Albert Client.

    Provides the same interface as AlbertClient but with async/await support.

    Example:
        ```python
        from albert_client import AsyncAlbertClient

        # Initialize async client
        client = AsyncAlbertClient(
            api_key="albert_...",
            base_url="https://albert.api.etalab.gouv.fr/v1"
        )

        # OpenAI-compatible endpoints
        response = await client.chat.completions.create(
            model="AgentPublic/llama3-instruct-8b",
            messages=[{"role": "user", "content": "Hello!"}]
        )

        # Albert-specific endpoints (coming in Phase 2+)
        # results = await client.search(prompt="...", collections=["..."])
        ```
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://albert.api.etalab.gouv.fr/v1",
        **kwargs,
    ):
        """Initialize async Albert client.

        Args:
            api_key: Albert API key. If not provided, reads from ALBERT_API_KEY env var.
            base_url: Base URL for Albert API (includes /v1 suffix).
            **kwargs: Additional arguments passed to AsyncOpenAI client.
        """
        # Get API key from env if not provided
        if api_key is None:
            api_key = os.environ.get("ALBERT_API_KEY")

        if not api_key:
            raise ValueError(
                "Albert API key is required. Provide via api_key parameter or "
                "ALBERT_API_KEY environment variable."
            )

        # Initialize wrapped AsyncOpenAI client
        self._client = AsyncOpenAI(api_key=api_key, base_url=base_url, **kwargs)

        # OpenAI-Compatible Passthrough
        self.chat = self._client.chat
        self.embeddings = self._client.embeddings
        self.audio = self._client.audio
        self.models = self._client.models

        # Albert-Specific Resources (will be implemented in Phase 2+)
        # self.collections = AsyncCollections(self._client)
        # self.documents = AsyncDocuments(self._client)
        # self.tools = AsyncTools(self._client)
        # self.management = AsyncManagement(self._client)

    @property
    def api_key(self) -> str:
        """Get the API key."""
        return self._client.api_key

    @property
    def base_url(self) -> str:
        """Get the base URL."""
        return str(self._client.base_url)

    async def close(self) -> None:
        """Close the underlying httpx client."""
        await self._client.close()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    # Phase 2: search() and rerank() async methods will be added here
