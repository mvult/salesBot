from datetime import datetime

import yagmail
import requests

from persistence.models import Message, Conversation
from config import SALES_BOT_MODE, EVENLIFT_IG_ID, IG_ACCESS_TOKEN, NOTIFICATION_EMAIL, NOTIFICATION_EMAIL_PASSWORD 

def send_message_to_user(m: Message, client_id: str):
    print(f"Sending '{m.content[:10]}'- message to {client_id} at {datetime.now()}")
    if SALES_BOT_MODE != "live":
        print(f"Would send message to insta, but in test mode {m.content}")
        return

    print(f"Sending to client_id {client_id} from {EVENLIFT_IG_ID} content: {m.content}")

    r = requests.post(f"https://graph.instagram.com/v22.0/{EVENLIFT_IG_ID}/messages", 
                  headers={"Authorization": f"Bearer {IG_ACCESS_TOKEN}", "Content-Type":"application/json"},           
                  params={'access_token': IG_ACCESS_TOKEN}, 
                  json={"recipient":{"id":client_id}, "message": {"text": m.content}})
    if not r.ok:
        raise Exception(f"Error sending message to user: {r.text}")



def send_email_to_operators(convo: Conversation, to: str = "rodrigo@evenlift.io"):
    if SALES_BOT_MODE != "live":
        print(f"Would send email to insta")
        return

    yag = yagmail.SMTP(NOTIFICATION_EMAIL, NOTIFICATION_EMAIL_PASSWORD)
    yag.send(
        to=to,
        subject= f"Salesbot handoff {convo.client_name} ID: {convo.client_id}",
        contents= f"Salesbot handoff {convo.client_name} ID: {convo.client_id}",
    )

    print("Email successfulyl sent")


def get_instagram_username_from_id(id: str) -> str:
    try:
        if SALES_BOT_MODE != "live":
            print(f"Would ping IG for user name")
            return "fake_name"

        r = requests.get(f"https://graph.instagram.com/v22.0/{id}", 
                    headers={"Authorization": f"Bearer {IG_ACCESS_TOKEN}", "Content-Type":"application/json"},           
                    params={'access_token': IG_ACCESS_TOKEN, 'fields':"id,username"}
                    )

        assert r.ok
        return r.json()['username']

    except Exception as e:
        print("Error getting username from id", e)
        return "Unknown"

