from persistence.models import Message, Conversation
from config import SALES_BOT_MODE

def send_message_to_user(m: Message):
    if SALES_BOT_MODE != "live":
        print(f"Would send message to insta, but in test mode {m.content}")
        return
    pass

def send_email_to_operators(convo: Conversation):
    if SALES_BOT_MODE != "live":
        print("Would send email to human operators, but in test mode")
        return

    print("Sending email to human operators")

    pass

