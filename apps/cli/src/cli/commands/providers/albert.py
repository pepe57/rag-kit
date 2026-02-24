"""Albert API provider for Data Foundry.

Uses Albert API (OpenGateLLM) for document ingestion, search, and Q/A generation.
Leverages the rag_facile pipeline packages (ingestion, storage, retrieval) for
consistency with the main RAG pipeline.
"""

import json
import logging
import time
from collections.abc import Iterator
from pathlib import Path

from .schema import GeneratedSample


logger = logging.getLogger(__name__)


class AlbertApiProvider:
    """Data Foundry provider using Albert API (OpenGateLLM).

    Uses the rag_facile pipeline packages for document processing, storage,
    and retrieval. This ensures consistency with the main RAG pipeline.

    The provider:
    1. Uploads documents to Albert collections (via storage provider)
    2. Searches collections using configured retrieval strategy
    3. Generates Q/A pairs from search results via LLM streaming

    All parameters (chunking, retrieval, generation) come from ragfacile.toml.
    """

    def __init__(self):
        """Initialize the Albert API provider."""
        from rag_facile.core import get_config
        from rag_facile.ingestion import get_provider as get_ingestion_provider
        from rag_facile.storage import get_provider as get_storage_provider

        self.config = get_config()
        self._ingestion = get_ingestion_provider(self.config)
        self._storage = get_storage_provider(self.config)

        # Lazily initialized on first use
        self._client = None
        self.collection_id: int | None = None

    @property
    def client(self):
        """Lazily create Albert client on first use."""
        if self._client is None:
            from albert import AlbertClient

            self._client = AlbertClient()
        return self._client

    def upload_documents(self, document_paths: list[str]) -> None:
        """Upload documents to Albert and create a collection.

        Uses the rag_facile storage provider for Albert collections, which
        respects chunking parameters from ragfacile.toml.

        Args:
            document_paths: List of paths to documents (PDF, MD, HTML)
        """
        logger.info(
            f"Starting document upload to Albert API ({len(document_paths)} documents)"
        )
        for doc_path in document_paths:
            logger.debug(f"  - {doc_path}")

        # Create a collection using the storage provider
        collection_name = f"data_foundry_{int(time.time() * 1000)}"
        self.collection_id = self._storage.create_collection(
            self.client,
            name=collection_name,
            description="RAG Facile Data Foundry",
        )
        logger.info(f"Created Albert collection: {self.collection_id}")

        # Upload documents using the storage provider
        # (which respects config.chunking.chunk_size and chunk_overlap)
        try:
            self._storage.ingest_documents(
                self.client,
                [Path(p) for p in document_paths],
                self.collection_id,
            )
            logger.info(
                f"Ingested {len(document_paths)} documents into collection {self.collection_id}"
            )
        except Exception as e:
            error_msg = f"Failed to ingest documents: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e

    def generate(self, num_samples: int) -> Iterator[GeneratedSample]:
        """Generate Q/A samples using retrieval from the collection and LLM.

        Args:
            num_samples: Target number of samples to generate

        Yields:
            GeneratedSample objects as they are generated
        """
        if not self.collection_id:
            raise RuntimeError(
                "No collection ID available. Call upload_documents first."
            )

        # Retrieve sample passages from the collection to ground the generation
        document_context = self._retrieve_document_context()

        # Build the generation prompt with document context
        prompt = self._build_prompt(num_samples, document_context)
        logger.debug(f"Generation prompt ({len(prompt)} chars):\n{prompt}\n")

        # Stream the response from LLM
        logger.info(f"Sending prompt to Albert API (collection: {self.collection_id})")
        seen_samples: set[str] = set()
        buffer = ""
        total_response = ""

        try:
            # Use the configured model for generation (defaults to openai/gpt-oss-120b)
            model = self.config.generation.model
            stream = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            )

            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    total_response += content
                    buffer += content

                    # Split into lines, keeping the last (possibly incomplete) line
                    lines = buffer.split("\n")
                    buffer = lines.pop()  # Keep incomplete line in buffer

                    # Process complete lines
                    for line in lines:
                        yield from self._process_line(line, seen_samples)

            # Process any remaining content in the buffer
            if buffer:
                yield from self._process_line(buffer, seen_samples)

            logger.info("Completed Albert generation")
            logger.debug(
                f"Total response ({len(total_response)} chars):\n{total_response}\n"
            )
        except Exception as e:
            logger.error(f"LLM generation failed: {e}", exc_info=True)
            raise RuntimeError(f"LLM generation failed: {e}") from e

    def _process_line(
        self, line: str, seen_samples: set[str]
    ) -> Iterator[GeneratedSample]:
        """Process a single line, yielding unique samples."""
        for sample in self._extract_samples(line):
            sample_key = sample.user_input
            if sample_key not in seen_samples:
                seen_samples.add(sample_key)
                yield sample

    def cleanup(self) -> None:
        """Delete collection from Albert API."""
        if self.collection_id:
            try:
                self._storage.delete_collection(self.client, self.collection_id)
            except Exception:
                pass  # Non-critical

    def _retrieve_document_context(self) -> str:
        """Retrieve sample passages from the collection to ground generation.

        Uses the rag_facile retrieval package with configured search strategy
        to get representative passages from the uploaded documents.

        Returns:
            A formatted string containing sample passages from the document
        """
        if not self.collection_id:
            return "[Document context not available]"

        try:
            from rag_facile.retrieval import search_chunks

            # Delay to allow document indexing in Albert
            time.sleep(2.0)

            # Use several broad search queries to capture different aspects
            search_queries = [
                "principaux points",
                "concepts clés",
                "objectifs",
                "informations",
                "contenu",
            ]

            passages = []
            for query in search_queries:
                try:
                    # Use the retrieval package with configured strategy
                    chunks = search_chunks(
                        self.client,
                        query,
                        [self.collection_id],
                        limit=2,
                        method=self.config.retrieval.strategy,
                        score_threshold=self.config.retrieval.score_threshold,
                    )

                    if chunks:
                        for chunk in chunks:
                            # Chunks are dicts with 'text' key
                            text = chunk.get("text", "")
                            if text and text not in passages:
                                passages.append(text[:500])  # Limit passage length
                except Exception as e:
                    logger.debug(f"Search for '{query}' failed: {e}")
                    continue

            if passages:
                context = "\n\n---\n\n".join(passages[:5])  # Max 5 passages
                return f"Sample passages from the document:\n\n{context}"
            else:
                return (
                    "A document has been uploaded to the collection. "
                    "Please generate Q/A pairs based on the document content, "
                    "ensuring each answer is grounded in the uploaded material."
                )

        except Exception as e:
            logger.warning(f"Failed to retrieve document context: {e}")
            return "[Document context retrieval failed. Proceeding without context.]"

    def _build_prompt(self, num_samples: int, document_context: str) -> str:
        """Build the generation prompt for the LLM with document context.

        Args:
            num_samples: Number of Q/A pairs to generate
            document_context: Sample passages from the document to ground generation

        Returns:
            The formatted prompt string
        """
        return f"""You are helping generate a synthetic evaluation dataset from a document.

DOCUMENT CONTEXT:
{document_context}

TASK:
Generate {num_samples} Question/Answer pairs (Q&A) based ONLY on the document context provided above.

REQUIREMENTS:
- All questions and answers MUST be in French
- Each answer must be grounded in and directly supported by the document passages shown
- Create diverse questions covering different aspects of the document
- For each Q&A pair, include the exact document passage that supports the answer

OUTPUT FORMAT:
Generate exactly {num_samples} JSON objects, one per line (JSONL format). Each object must have this structure:
{{
  "user_input": "Question in French?",
  "retrieved_contexts": ["The exact document passage supporting this answer"],
  "reference": "Answer in French, supported by the context above",
  "_metadata": {{
    "source_file": "document.pdf",
    "quality_score": 0.85,
    "topic_summary": "Brief topic description"
  }}
}}

Output ONLY the JSON lines with no additional text, explanations, or preamble. Start directly with the first JSON object.
Generate exactly {num_samples} Q&A pairs."""

    def _extract_samples(self, line: str) -> Iterator[GeneratedSample]:
        """Extract JSON sample from a single line."""
        line = line.strip()
        if not line or not line.startswith("{"):
            return

        try:
            data = json.loads(line)
            if "user_input" in data and "reference" in data:
                yield GeneratedSample.from_dict(data)
        except json.JSONDecodeError:
            pass  # Incomplete JSON, skip
