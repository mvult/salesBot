import asyncio
from datetime import datetime, UTC

from messaging.utils import calculate_typing_delay_seconds
from sqlalchemy import select
from sqlalchemy.orm import Session

from pydanticModels import IGMessagePayloadSchema 
from persistence.models import Conversation, Message
from persistence.db import get_async_db
from config import EVENLIFT_IG_ID, SALES_BOT_MODE
from llm.hooks import generate_llm_message 
from messaging.bundling import add_bundle_info, split_llm_response, bundle_messages
from messaging.external import send_message_to_user 
from messaging.utils import calculate_typing_delay_seconds, handoff, get_relevant_conversation, MESSAGE_ACCUMULATION_SECONDS, should_skip_message, get_client_id, message_already_seen


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

        if len(msgs) == 0: return 

        latest = msgs[-1]

        _convo = await db.execute(select(Conversation).filter_by(id=convo_id))
        convo = _convo.scalars().one()

        if any(m.has_attachment and m.role == "user" for m in msgs):
            print("Message has attachment")
            if not convo.handed_off:
                print("Handing off")
                await handoff(convo, db)
            return

        if should_skip_message(convo, latest):
            print("SKIPPING")
            return

        print("NOT SKIPPING")
        msgs = add_bundle_info(list(msgs))

        try:
            bundled_msgs = bundle_messages(list(msgs))
            llm_response, hand_off, skip_message = generate_llm_message(bundled_msgs, convo.agent_id)

            if hand_off:
                print("HANDING OFF")
                await handoff(convo, db)
            if skip_message:
                print("SKIPPING DUE TO LLM ERROR")
                return

        except Exception as e:
            print("Unknown error generating llm response", e)
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

        for i, m in enumerate(new_msgs):
            try:
                if SALES_BOT_MODE == "live" and i != 0:
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

    m = Message(conversation_id=convo.id, content=event.get_text_content(), role="user", source="ig", sender_id=sender_id, recipient_id=recipient_id, has_attachment=event.has_attachment())

    convo.most_recent_user_message = datetime.now()
    session.add(m)
    session.commit()
    session.refresh(convo)

    return convo
 


def handle_message_from_evenlift(event: IGMessagePayloadSchema, session: Session):
    client_id, sender_id, recipient_id = get_client_id(event)
    
    print(f"\n\nclient_id: {client_id}, sender_id: {sender_id}, recipient_id: {recipient_id}\n\n")

    convo = get_relevant_conversation(client_id, session)

    m = Message(conversation_id=convo.id, content=event.get_text_content(), role="assistant", source="ig", sender_id=sender_id, recipient_id=recipient_id, has_attachment=event.has_attachment())

    msgs = session.query(Message).filter_by(conversation_id=convo.id).filter_by(role="assistant").all()

    if message_already_seen(m, msgs):
        print("Message already seen, skipping")
        return
    else:
        convo.handed_off = True
        session.add(m)
        session.commit()
        session.refresh(convo)
        return 




