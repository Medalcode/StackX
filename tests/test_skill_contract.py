"""Tests for AI skill contract and fallback behavior."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_fallback_justification():
    import asyncio

    from backend.app import ai_client

    user_input = {'weights': {'backend': 1}, 'proyecto': 'Demo'}
    top_stack = {'name': 'FastAPI'}

    text = asyncio.run(ai_client.generate_justification(user_input, top_stack))

    assert isinstance(text, str)
    assert len(text) > 0
    assert "FastAPI" in text or "1)" in text


def test_generate_justification_with_ollama_unreachable(monkeypatch):
    monkeypatch.setenv("OLLAMA_URL", "http://localhost:1")
    import asyncio

    from backend.app import ai_client

    user_input = {'weights': {'backend': 1}, 'proyecto': 'Demo'}
    top_stack = {'name': 'FastAPI'}

    text = asyncio.run(ai_client.generate_justification(user_input, top_stack))
    assert isinstance(text, str)
    assert len(text) > 0


def test_skill_content_generator():
    import asyncio

    from backend.app.ai_skills import content_generator

    result = asyncio.run(content_generator.run_skill({
        "mode": "full_justification",
        "tech": {"name": "FastAPI"},
    }))
    assert result["status"] == "ok"
    assert "FastAPI" in result["result"]["text"]


def test_skill_content_generator_concise():
    import asyncio

    from backend.app.ai_skills import content_generator

    result = asyncio.run(content_generator.run_skill({
        "mode": "concise_summary",
        "tech": {"name": "Go"},
    }))
    assert result["status"] == "ok"
    assert "Go" in result["result"]["text"]


def test_skill_data_analysis():
    import asyncio

    from backend.app.ai_skills import data_analysis

    result = asyncio.run(data_analysis.run_skill({
        "operation": "calculate_stack_score",
        "tech": {"name": "FastAPI"},
    }))
    assert result["status"] == "ok"
    assert "score" in result["result"]


def test_skill_data_analysis_unsupported():
    import asyncio

    from backend.app.ai_skills import data_analysis

    result = asyncio.run(data_analysis.run_skill({
        "operation": "unknown_op",
    }))
    assert result["status"] == "ok"
    assert "error" in result["result"]
