from typing import cast
from datetime import datetime, timedelta, timezone
import re

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from persistence.models import Conversation, Message
from messaging.external import send_email_to_operators
from agents.hooks import get_optimized_agent
from pydanticModels import IGMessagePayloadSchema
from config import EVENLIFT_IG_ID, SALES_BOT_MODE 
from messaging.external import get_instagram_username_from_id

MESSAGE_ACCUMULATION_SECONDS = 7

def calculate_typing_delay_seconds(message: str) -> float:
    num_chars = len(message) / 1.5
    total_delay = (num_chars * 0.1) + ((num_chars - 1) // 20 * 0.5)
    print(f"Delay for {len(message)} chars: {total_delay}")
    return total_delay  # Returns delay in seconds

async def handoff(convo: Conversation, db: AsyncSession):
    convo.handed_off = True
    await db.commit()
    send_email_to_operators(cast(Conversation, convo))


def get_relevant_conversation(client_id: str, session: Session) -> Conversation: 
        try:
            return session.query(Conversation).filter_by(client_id=client_id).one()
        except NoResultFound:
            print("creating new convo for user", client_id)
            new_convo = Conversation(
                client_id=client_id,
                platform="ig",
                agent_id=get_optimized_agent(session).id,
                client_name=get_instagram_username_from_id(client_id)
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


def message_already_seen(m: Message, msgs: list[Message]) -> bool:
    def normalize_string(s):
        s = re.sub(r'[^\w\s]', '', s)  # Keep words and spaces temporarily
        s = re.sub(r'\s+', '', s)      # Remove all spaces after punctuation is gone
        s = s.encode('ascii', 'ignore').decode('ascii')  # Strip emojis/non-ASCII
        return s.lower()

    def are_strings_pretty_similar(s1, s2):
        return normalize_string(s1) == normalize_string(s2)

    return any(are_strings_pretty_similar(m.content, msg.content) for msg in msgs)
