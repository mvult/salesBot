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

def pytest_addoption(parser):
    parser.addoption(
        "--run-external", action="store_true", default=False, help="Run tests marked as external"
    )

def pytest_collection_modifyitems(config, items):
    if not config.getoption("--run-external"):
        skip_external = pytest.mark.skip(reason="Requires --run-external option to run")
        for item in items:
            if "external" in item.keywords:
                item.add_marker(skip_external)
