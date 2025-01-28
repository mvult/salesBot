import requests 
import datetime
import time
import uuid

def msg_payload(sender_id, recipient_id, message):
    return {
        "entry": [
            {
                "id": "0",
                "time": int(datetime.datetime.now().timestamp()),
                "messaging": [
                    {
                        "message": {"mid": "an_id","text": "this is a message"},
                        "sender": {
                            "id": sender_id
                        },
                        "recipient": {
                            "id": recipient_id
                        },
                        "timestamp": int(datetime.datetime.now().timestamp()),
                    }
                ]
            }
        ],
        "object": "instagram"
    }

def test_post_webhook_instagram(base_url, headers):

    r = requests.post(f"{base_url}/webhooks", headers=headers,json=msg_payload("640673465068123","17841411286042347", "Hello there"))
    print(r.json())
    assert r.status_code == 200
    
    r = requests.post(f"{base_url}/webhooks", headers=headers,json=msg_payload("23245","12334", "Hello yourself"))
    assert r.status_code == 200




def test_multiple_messages(base_url, headers, evenlift_ig_id):
    new_user_id = str(uuid.uuid4())
    r = requests.post(f"{base_url}/webhooks", headers=headers,json=msg_payload(new_user_id, evenlift_ig_id, "Hello there"))

    assert r.status_code == 200

    time.sleep(1)
    r = requests.post(f"{base_url}/webhooks", headers=headers,json=msg_payload(new_user_id, evenlift_ig_id, "Second message"))

    assert r.status_code == 200

    # get coversation based on client_id
    r = requests.get(f"{base_url}/conversations?client_id={new_user_id}", headers=headers)
    assert r.status_code == 200

    print(r.json())
    id = r.json()[0]['id']

    time.sleep(4)
    r = requests.get(f"{base_url}/conversations/{id}/messages", headers=headers)
    print(r.json())

    assert len(r.json()) == 3
    assert r.json()[0]['role'] == "user"
    assert r.json()[0]['role'] == "user"
    assert r.json()[2]['role'] == "assistant"
    
    assert r.json()[0]['bundle_id'] == r.json()[1]['bundle_id']
    

    
    
