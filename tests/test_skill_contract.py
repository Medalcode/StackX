import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_example_skill_contract():
    # For the contract test we point JUSTIFICATION_SKILL to the example skill
    os.environ['JUSTIFICATION_SKILL'] = 'example_justification'

    from backend.app import ai_client

    user_input = {'weights': {'backend': 1}, 'proyecto': 'Demo', 'request_id': 'test-1'}
    top_stack = {'name': 'FastAPI'}

    text = ai_client.generate_justification(user_input, top_stack)

    assert isinstance(text, str)
    assert len(text) > 0
