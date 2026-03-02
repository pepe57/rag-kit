# memory

Flat-file persistent memory for the rag-facile chat agent.

## Architecture

All state is stored as plain Markdown files under `.rag-facile/agent/`:

```
.rag-facile/agent/
├── memory.md           # Semantic store — curated facts with fixed sections
├── profile.md          # User profile (language, experience, session count)
├── logs/
│   └── YYYY-MM-DD.md   # Episodic logs — append-only daily transcripts
└── sessions/
    └── *.md            # Session snapshots — archived full transcripts
```

## Retrieval

Search uses pure Python `re` + `glob` (no SQLite, no embeddings). The agent
has two tools:

- `grep_memory(query)` — keyword search across all `.md` files
- `read_memory_lines(file, start, end)` — read context around a hit

## Dependencies

**Zero external dependencies** — stdlib only (`re`, `pathlib`, `glob`, `hashlib`).
