# RAG Configuration Guide

This guide provides a comprehensive overview of the RAG Configuration System in RAG Facile. It covers the available configuration sections, environment variable overrides, and management via the CLI.

## Overview

RAG Facile uses a centralized configuration system based on `ragfacile.toml`. This allows you to customize every aspect of your RAG pipeline—from how documents are chunked to how the LLM generates responses—without changing a single line of code.

## The 13 Configuration Sections

The configuration is organized into 13 functional sections, reflecting the typical RAG pipeline:

### 1. `meta`
Metadata about the configuration file.
- `schema_version`: Version of the config schema (e.g., "1.0.0").
- `preset`: The active preset name (e.g., "balanced").

### 2. `eval`
Settings for synthetic Q/A dataset generation (Data Foundry).
- `provider`: `letta` or `albert`.
- `target_samples`: Number of Q/A pairs to generate (default: 50).

### 3. `ingestion`
How documents are processed before chunking.
- `ocr`: OCR settings for scanned PDFs.
- `parsing`: Preserve structure (headings, lists, tables) and output format.

### 4. `chunking`
Strategies for splitting text into manageable pieces.
- `strategy`: `fixed-size`, `semantic`, `sentence`, or `paragraph`.
- `chunk_size`: Size in tokens or characters.
- `chunk_overlap`: Overlap between adjacent chunks.

### 5. `embedding`
Configuration for generating vector representations.
- `model`: Model name (e.g., `albert-embedding-small`).
- `batch_size`: Number of chunks processed at once.

### 6. `storage`
Where vectors are stored and how they are indexed.
- `backend`: `albert-collections`, `chroma`, or `local-sqlite`.
- `distance_metric`: `cosine`, `euclidean`, or `dot-product`.

### 7. `query`
Enhancements applied to the user's query before retrieval.
- `rewrite_enabled`: Rewrites queries for better clarity.
- `expand_enabled`: Adds synonyms or related terms.

### 8. `retrieval`
How relevant document chunks are found.
- `method`: `hybrid` (recommended), `semantic`, or `lexical`.
- `top_k`: Number of chunks to retrieve initially.
- `score_threshold`: Minimum relevance score (0.0 to 1.0).

### 9. `reranking`
Refines the initial retrieval results for higher precision.
- `enabled`: Toggle reranking on/off.
- `model`: Reranker model (e.g., `bge-reranker-large`).
- `top_n`: Final number of chunks to keep after reranking.

### 10. `context`
Manages the context window sent to the LLM.
- `max_tokens`: Total token budget for context.
- `strategy`: `token-budget`, `top-n`, or `threshold`.
- `include_citations`: Automatically adds source indices.

### 11. `generation`
Settings for the Large Language Model (LLM).
- `model`: Model name (e.g., `openweight-medium`).
- `temperature`: Creativity vs. determinism (0.0 to 2.0).
- `system_prompt`: The core instructions for the AI.

### 12. `hallucination`
Validation layers to ensure response accuracy.
- `enabled`: Toggle hallucination detection.
- `method`: `citation-check`, `fact-check`, or `entailment`.
- `fallback`: Behavior if hallucination is detected (`warn`, `reject`, `regenerate`).

### 13. `formatting`
Settings for how the final answer is presented to the user.
- `output_format`: `markdown`, `html`, or `plain-text`.
- `include_sources`: Toggle inclusion of a sources list at the end.
- `language`: The language of the generated response (`fr` or `en`).

## Environment Variable Overrides

Any setting in `ragfacile.toml` can be overridden by environment variables using the `RAG_<SECTION>_<KEY>` format.

### Naming Convention
- **Uppercase**: All characters must be uppercase.
- **Underscore Separator**: Use underscores between parts.
- **Nested Keys**: For nested settings (like `ingestion.ocr.enabled`), use `RAG_INGESTION_OCR_ENABLED`.

### Examples
```bash
# Override the model
export RAG_GENERATION_MODEL=openweight-large

# Change retrieval top_k
export RAG_RETRIEVAL_TOP_K=20

# Disable reranking
export RAG_RERANKING_ENABLED=false
```

### Precedence
1. **Environment Variables** (Highest precedence)
2. **`ragfacile.toml`** (Project-level config)
3. **Preset Defaults** (Base values)

## CLI Management

Use the `rag-facile config` command group to manage your settings:

- `rag-facile config show`: View current settings (including active overrides).
- `rag-facile config set <key> <value>`: Update a setting in `ragfacile.toml`.
- `rag-facile config validate`: Check for errors or suboptimal settings.
- `rag-facile config preset list`: See available battle-tested presets.
- `rag-facile config preset apply <name>`: Reset your config to a specific preset.

## Best Practices

1. **Keep Secrets Secret**: Never put API keys in `ragfacile.toml`. Use `.env` files or system environment variables.
2. **Use Presets**: Start with `balanced` or `accurate` and tune from there.
3. **Validate Often**: Run `rag-facile config validate` after making manual edits to the TOML file.
4. **Environment-Specific Config**: Use environment variables in CI/CD or production to override development settings without changing the repo's config file.
