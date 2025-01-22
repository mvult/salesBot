import requests 
import datetime

def msg_payload(sender_id, recipient_id, message):
    return {
        "entry": [
            {
                "id": "0",
                "time": int(datetime.datetime.now().timestamp()),
                "changes": [
                    {
                        "field": "messages",
                        "value": {
                            "sender": {
                                "id": sender_id
                            },
                            "recipient": {
                                "id": recipient_id
                            },
                            "timestamp": f"{int(datetime.datetime.now().timestamp())}",
                            "message": {
                                "mid": "random_mid",
                                "text": message
                            }
                        }
                    }
                ]
            }
        ],
        "object": "instagram"
    }

def test_post_webhook_instagram(base_url, headers):
    r = requests.post(f"{base_url}/webhooks", headers=headers,json=msg_payload("12334", "23245", "Hello there"))
    print(r.json())
    assert r.status_code == 200
    
    r = requests.post(f"{base_url}/webhooks", headers=headers,json=msg_payload("23245","12334", "Hello yourself"))
    assert r.status_code == 200
