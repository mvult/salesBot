import pytest
import requests
import json

@pytest.fixture
def base_url():
    return "http://localhost:8000"

@pytest.fixture
def headers():
    return {"Content-Type": "application/json"}

@pytest.fixture
def test_agent_data():
    return {
        "name": "Test Agent",
        "instructions": "Test agent description",
    }

def test_post_agent(base_url, headers, test_agent_data):
    response = requests.post(
        f"{base_url}/agents",
        headers=headers,
            json=test_agent_data
        )

    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["name"] == test_agent_data["name"]

def test_get_agents(base_url, headers):
        # Test getting all agents
    response = requests.get(f"{base_url}/agents", headers=headers)
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    print(response.json())

def test_post_webhook(base_url, headers):
    r = requests.post(base_url + "/webhooks", headers=headers, json={"key": "value"})
    print(r.json())
