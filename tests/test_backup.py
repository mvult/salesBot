import pytest

from llm.backup import get_response_from_open_ai
from persistence.models import Message

@pytest.mark.external
def test_open_ai():
    r = get_response_from_open_ai([Message(role="user", content="Hello")], "Test system", "You are a robot that responds with a poem")
    print(r)
