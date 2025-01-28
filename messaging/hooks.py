import asyncio
from datetime import datetime, timedelta, UTC, timezone
from typing import cast

from messaging.utils import calculate_typing_delay_seconds
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import select
from sqlalchemy.orm import Session

from pydanticModels import IGMessagePayloadSchema 
from persistence.models import Conversation, Message
from persistence.db import get_async_db
from config import EVENLIFT_IG_ID, SALES_BOT_MODE
from agents.hooks import get_optimized_agent
from llm import generate_llm_message, HANDOFF_MESSAGE
from messaging.bundling import add_bundle_info, split_llm_response, bundle_messages
from messaging.external import send_message_to_user, send_email_to_operators
from messaging.utils import calculate_typing_delay_seconds

MESSAGE_ACCUMULATION_SECONDS = 7

async def evaluate_conversation(convo_id: int, client_id: str):
    print("In async!")
    if SALES_BOT_MODE == "live":
        await asyncio.sleep(MESSAGE_ACCUMULATION_SECONDS + 5)
    else:
        await asyncio.sleep(3)

    print("After sleep!")

    async with get_async_db() as db:
        _msgs = await db.execute(select(Message).filter_by(conversation_id=convo_id).order_by(Message.create_time))
        
        msgs = _msgs.scalars().all()

        if len(msgs) == 0:return 

        latest = msgs[-1]

        _convo = await db.execute(select(Conversation).filter_by(id=convo_id))
        convo = _convo.scalars().one()

        if should_skip_message(convo, latest):
            print("SKIPPING")
            return

        print("NOT SKIPPING")
        msgs = add_bundle_info(list(msgs))

        try:
            bundled_msgs = bundle_messages(list(msgs))
            llm_response = generate_llm_message(bundled_msgs, convo.agent_id)
            if llm_response == HANDOFF_MESSAGE:
                convo.handed_off = True
                await db.commit()
                send_email_to_operators(cast(Conversation, convo))

        except Exception as e:
            print("Error generating llm response", e)
            raise e

        new_msg_texts = split_llm_response(llm_response)
        
        print(f"Split the following text: \n${llm_response}\nInto the following messages:\n${new_msg_texts}")

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
                send_message_to_user(m, convo.client_id)
                m.create_time = datetime.now(UTC)
                db.add(m)
                await db.commit()
            except Exception as e:
                print("Error sending message to user:", e)
                raise e


        
def receive_message_event(event: IGMessagePayloadSchema, session:Session) -> Conversation:
    client_id, sender_id, recipient_id = get_client_id(event)
    
    print(f"\n\nclient_id: {client_id}, sender_id: {sender_id}, recipient_id: {recipient_id}\n\n")

    convo = get_relevant_conversation(client_id, session)

    m = Message(conversation_id=convo.id, content=event.get_text_content(), role="user", source="ig", sender_id=sender_id, recipient_id=recipient_id)

    session.add(m)
    session.commit()
    session.refresh(convo)
    
    return convo
    

def get_relevant_conversation(client_id: str, session: Session) -> Conversation: 
        try:
            return session.query(Conversation).filter_by(client_id=client_id).one()
        except NoResultFound:
            print("creating new convo for user", client_id)
            new_convo = Conversation(
                client_id=client_id,
                platform="ig",
                agent_id=get_optimized_agent(session).id,
            )
            session.add(new_convo)
            session.flush()
            return new_convo
        except MultipleResultsFound:
            raise Exception("Multiple conversations found for client_id", client_id)

        except Exception as e:
            print("Unexpected Error", e)
            raise e

        

def get_client_id(event: IGMessagePayloadSchema) -> tuple[str, str, str]:
    sender_id = event.get_sender_id()
    recipient_id = event.get_recipient_id()
    if sender_id != EVENLIFT_IG_ID:
        return sender_id, sender_id, recipient_id
    return recipient_id, sender_id, recipient_id

def should_skip_message(convo: Conversation, lastMsg: Message) -> bool:
    if convo.handed_off:
        print(f"Convo {convo.client_id} {convo.client_name} already handed off to human")
        return True
    
    if lastMsg.role == "assistant":
        print("Last message was from assistant, skipping")
        return True


    now = datetime.now(timezone.utc).replace(tzinfo=None)
    time_since_last_msg = now - lastMsg.create_time
    accumulation_time = MESSAGE_ACCUMULATION_SECONDS if SALES_BOT_MODE == "live" else 2

    print(time_since_last_msg, accumulation_time)

    if time_since_last_msg < timedelta(seconds=accumulation_time):
        print("Skipping message, not enough time has passed since last message")
        return True 

    return False
