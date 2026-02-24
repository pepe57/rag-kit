"""Tests for the inject_rag_context solver."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from inspect_ai.model import ChatMessageUser

from rag_facile.evaluation._solvers import inject_rag_context


@pytest.mark.asyncio
async def test_inject_context_prepends() -> None:
    """Context is prepended to the user message."""
    solver = inject_rag_context()
    state = MagicMock()
    state.metadata = {
        "retrieved_contexts": ["Context A", "Context B"],
    }
    state.input_text = "What is RAG?"
    state.messages = [ChatMessageUser(content="What is RAG?")]

    result = await solver(state, generate=None)

    first_msg = result.messages[0]
    assert isinstance(first_msg, ChatMessageUser)
    assert "Context A" in first_msg.content
    assert "Context B" in first_msg.content
    assert "What is RAG?" in first_msg.content
    # Context appears before the question
    assert first_msg.content.index("Context A") < first_msg.content.index(
        "What is RAG?"
    )


@pytest.mark.asyncio
async def test_inject_no_context() -> None:
    """When no contexts, messages are unchanged."""
    solver = inject_rag_context()
    original_msg = ChatMessageUser(content="What is RAG?")
    state = MagicMock()
    state.metadata = {"retrieved_contexts": []}
    state.messages = [original_msg]

    result = await solver(state, generate=None)

    assert result.messages[0] is original_msg
