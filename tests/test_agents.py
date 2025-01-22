import pytest
import requests
import json

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

def test_post_webhook(base_url, headers):
    r = requests.post(base_url + "/webhooks", headers=headers, json={"key": "value"})
    print(r.json())


def test_post_webhook_instagram(base_url, headers):
    json_payload = {
        "entry": [
            {
                "id": "0",
                "time": 1737484299,
                "changes": [
                    {
                        "field": "messages",
                        "value": {
                            "sender": {
                                "id": "12334"
                            },
                            "recipient": {
                                "id": "23245"
                            },
                            "timestamp": "1527459824",
                            "message": {
                                "mid": "random_mid",
                                "text": "random_text"
                            }
                        }
                    }
                ]
            }
        ],
        "object": "instagram"
    }

    r = requests.post(
        f"{base_url}/webhooks",
        headers=headers,
        json=json_payload
    )

    assert r.status_code == 200
