"""Main Albert Client implementation."""

import os

from openai import OpenAI


class AlbertClient:
    """Official Python SDK for France's Albert API.

    Provides OpenAI-compatible endpoints (chat, embeddings, audio, models) and
    Albert-specific endpoints (search, rerank, collections, documents, tools, management).

    Example:
        ```python
        from albert_client import AlbertClient

        # Initialize client
        client = AlbertClient(
            api_key="albert_...",  # Or set ALBERT_API_KEY env var
            base_url="https://albert.api.etalab.gouv.fr/v1"
        )

        # OpenAI-compatible endpoints
        response = client.chat.completions.create(
            model="AgentPublic/llama3-instruct-8b",
            messages=[{"role": "user", "content": "Hello!"}]
        )

        # Albert-specific endpoints (coming in Phase 2+)
        # results = client.search(prompt="...", collections=["..."])
        ```

    Architecture:
        - Wraps internal OpenAI client for OpenAI-compatible endpoints
        - Provides custom implementations for Albert-specific features
        - All responses use Pydantic models for type safety
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://albert.api.etalab.gouv.fr/v1",
        **kwargs,
    ):
        """Initialize Albert client.

        Args:
            api_key: Albert API key. If not provided, reads from ALBERT_API_KEY env var.
            base_url: Base URL for Albert API (includes /v1 suffix).
            **kwargs: Additional arguments passed to OpenAI client (timeout, max_retries, etc.).
        """
        # Get API key from env if not provided
        if api_key is None:
            api_key = os.environ.get("ALBERT_API_KEY")

        if not api_key:
            raise ValueError(
                "Albert API key is required. Provide via api_key parameter or "
                "ALBERT_API_KEY environment variable."
            )

        # Initialize wrapped OpenAI client
        self._client = OpenAI(api_key=api_key, base_url=base_url, **kwargs)

        # OpenAI-Compatible Passthrough (direct proxy to internal client)
        self.chat = self._client.chat
        self.embeddings = self._client.embeddings
        self.audio = self._client.audio
        self.models = self._client.models

        # Albert-Specific Resources (will be implemented in Phase 2+)
        # self.collections = Collections(self._client)
        # self.documents = Documents(self._client)
        # self.tools = Tools(self._client)
        # self.management = Management(self._client)

    @property
    def api_key(self) -> str:
        """Get the API key."""
        return self._client.api_key

    @property
    def base_url(self) -> str:
        """Get the base URL."""
        return str(self._client.base_url)

    # Phase 2: search() and rerank() methods will be added here
