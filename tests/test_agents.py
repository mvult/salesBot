import pytest
import requests

@pytest.fixture
def test_agent_data():
    return {
        "name": "Test Agent",
        "instructions": "Test agent description",
        "model": "very smart model",
        "tools": ["hey", "hello"],
        "identity": "a very nice model"
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


