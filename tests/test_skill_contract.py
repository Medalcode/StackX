import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_fallback_justification():
    from backend.app import ai_client

    user_input = {'weights': {'backend': 1}, 'proyecto': 'Demo'}
    top_stack = {'name': 'FastAPI'}

    text = ai_client.generate_justification(user_input, top_stack)

    assert isinstance(text, str)
    assert len(text) > 0
    assert "FastAPI" in text or "1)" in text


def test_generate_justification_with_ollama_unreachable(monkeypatch):
    """When OLLAMA_URL is set but unreachable, should fall back to template."""
    monkeypatch.setenv("OLLAMA_URL", "http://localhost:1")
    from backend.app import ai_client

    user_input = {'weights': {'backend': 1}, 'proyecto': 'Demo'}
    top_stack = {'name': 'FastAPI'}

    text = ai_client.generate_justification(user_input, top_stack)
    assert isinstance(text, str)
    assert len(text) > 0
