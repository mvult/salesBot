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
    
def test_bad_message(base_url, headers):
    r = requests.post(f"{base_url}/webhooks", headers=headers,json={"bad_json":"yes yes very bad"})

    assert r.status_code == 422
    
 # {'object': 'instagram', 'entry': [{'time': 1738201221115, 'id': '17841411286042347', 'messaging': [{'sender': {'id': '640673465068123'}, 'recipient': {'id': '17841411286042347'}, 'timestamp': 1738201220041, 'message': {'mid': 'aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDExMjg2MDQyMzQ3OjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTc5MDAxNjg2MzY1Mjc2NTozMjA2NDE1MzA1NDcyMDQ3Mjg1MjIxNTk3NzcxNTE3MTMyOAZDZD', 'attachments': [{'type': 'audio', 'payload': {'url': 'https://lookaside.fbsbx.com/ig_messaging_cdn/?asset_id=1627362851197033&signature=AbwllCYu_19jkUey_dTnSDc-QtFVlLLgPescKWvy_hbP8CjrNBEKvO_CaaDpESAWU7O-JsJZWVQZxs3a4FqlTSb-h3WIRNxa390wU7cXODHKeCT3GOH67ptCQr_guDwEL9Es-fkKXygxWDCtcBuY3Wz3iXKKjw4vdMk1936ttVvOR81GMx9ycJnMNN8oKJqR60nacWlyGnnC0gwm7kEnXitnTFnc5Zk'}}]}}]}]}


