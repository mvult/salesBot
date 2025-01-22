import asyncio
from datetime import datetime, timedelta, UTC

from messaging.utils import calculate_typing_delay_seconds
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from pydanticModels import WebhookPayloadSchema
from persistence.models import Conversation, Message
from persistence.db import get_db, get_async_db
from config import EVENLIFT_IG_ID, SALES_BOT_MODE
from agents.hooks import get_optimized_agent
from llm import generate_llm_message, HANDOFF_MESSAGE
from messaging.bundling import add_bundle_info, split_llm_response, bundle_messages
from messaging.external import send_message_to_user, send_email_to_operators
from messaging.utils import calculate_typing_delay_seconds

MESSAGE_ACCUMULATION_SECONDS = 25

async def evaluate_conversation(convo_id: int, client_id: str):
    print("In async!")
    if SALES_BOT_MODE == "live":
        await asyncio.sleep(MESSAGE_ACCUMULATION_SECONDS + 5)
    print("After sleep!")

    async with get_async_db() as db:
        msgs = db.query(Message).filter_by(conversation_id=convo_id).order_by(Message.create_time).all()
        latest = msgs[-1]

        if latest.role != "user" or (datetime.now(UTC) - latest.create_time) < timedelta(MESSAGE_ACCUMULATION_SECONDS):
            return

        convo = db.query(Conversation).filter_by(id=convo_id).first()
        if convo.handedOff:
            print(f"Convo {convo.client_id} {convo.client_name} already handed off to human")
            return

        msgs = add_bundle_info(msgs)

        try:
            bundled_msgs = bundle_messages(msgs)
            llm_response = generate_llm_message(bundled_msgs, convo.agent_id)
            if llm_response == HANDOFF_MESSAGE:
                convo.handedOff = True
                await db.commit()
                send_email_to_operators(convo)

        except Exception as e:
            print("Error generating llm response", e)
            raise e

        new_msg_texts = split_llm_response(llm_response)

        new_msgs = [Message(content=m, 
                            conversation_id=convo_id, 
                            role="assistant", 
                            source="llm", 
                            sender_id=EVENLIFT_IG_ID,
                            recipient_id=client_id,
                            ) for m in new_msg_texts]

        for m in new_msgs:
            try:
                if SALES_BOT_MODE == "live":
                    await asyncio.sleep(calculate_typing_delay_seconds(m.content))
                send_message_to_user(m)
                m.create_time = datetime.now(UTC)
                db.add(m)
                await db.commit()
            except Exception as e:
                print("Error sending message to user:", e)
                raise e


        
def receive_message_event(event: WebhookPayloadSchema) -> Conversation:
    client_id, sender_id, recipient_id = get_client_id(event)
    convo = get_relevant_conversation(client_id)

    m = Message(conversation_id=convo.id, content=event.entry[0].messaging[0].message.text, role="user", source="ig", sender_id=sender_id, recipient_id=recipient_id)

    with get_db() as session:
        session.add(m)
        session.commit()
    
    return convo
    

def get_relevant_conversation(client_id: str) -> Conversation: 
    with get_db() as session:
        try:
            return session.query(Conversation).filter_by(client_id=client_id).one()
        except NoResultFound:
            with get_db() as session:
                new_convo = Conversation(
                    client_id=client_id,
                    platform="ig",
                    agent_id=get_optimized_agent(session).id,
                )
                session.add(new_convo)
                session.commit()
                return new_convo
        except MultipleResultsFound:
            raise Exception("Multiple conversations found for client_id", client_id)

        

def get_client_id(event: WebhookPayloadSchema) -> tuple[str, str, str]:
    sender_id = event.entry[0].messaging[0].sender.id
    recipient_id = event.entry[0].messaging[0].recipient.id
    if sender_id != EVENLIFT_IG_ID:
        return sender_id, sender_id, recipient_id
    return recipient_id, sender_id, recipient_id


