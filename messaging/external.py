import requests
import yagmail

from persistence.models import Message, Conversation
from config import SALES_BOT_MODE, EVENLIFT_IG_ID, IG_ACCESS_TOKEN, NOTIFICATION_EMAIL, NOTIFICATION_EMAIL_PASSWORD 

def send_message_to_user(m: Message, client_id: str):
    if SALES_BOT_MODE != "live":
        print(f"Would send message to insta, but in test mode {m.content}")
        return

    print(f"Sending to client_id {client_id} from {EVENLIFT_IG_ID}")

    r = requests.post(f"https://graph.instagram.com/v22.0/{EVENLIFT_IG_ID}/messages", 
                  headers={"Authorization": f"Bearer {IG_ACCESS_TOKEN}", "Content-Type":"application/json"},           
                  params={'access_token': IG_ACCESS_TOKEN}, 
                  json={"recipient":{"id":client_id}, "message": {"text": m.content}})
    if not r.ok:
        raise Exception(f"Error sending message to user: {r.text}")



def send_email_to_operators(convo: Conversation, to: str = "rodrigo@evenlift.io"):
    print("Sending email")
    yag = yagmail.SMTP(NOTIFICATION_EMAIL, NOTIFICATION_EMAIL_PASSWORD)
    yag.send(
        to=to,
        subject= f"Salesbot handoff {convo.client_name} ID: {convo.client_id}",
        contents= f"Salesbot handoff {convo.client_name} ID: {convo.client_id}",
    )

    print("Email successfulyl sent")


