import os

import pytest
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture
def base_url():
    return "http://localhost:8000"

@pytest.fixture
def headers():
    return {"Content-Type": "application/json"}

@pytest.fixture
def evenlift_ig_id():
    return os.getenv("EVENLIFT_IG_ID")
