import pytest

@pytest.fixture
def base_url():
    return "http://localhost:8000"

@pytest.fixture
def headers():
    return {"Content-Type": "application/json"}
