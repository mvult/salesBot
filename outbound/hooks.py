from datetime import datetime, timedelta

from sqlalchemy import select, and_, desc
from sqlalchemy.orm import Session

from persistence.models import Conversation, Message
from outbound.build_messages import build_conversation_prompt


def send_reactivation_outbound(db: Session):
    conversations = get_pending_assistant_conversations(db)
    print(conversations)
    for c in conversations:
        prompt = build_conversation_prompt(db, c)
        print(prompt)
        # send_message(c.client_id, prompt)
        # print(f"Sent reactivation message to {c.client_id}")
    

def get_pending_assistant_conversations(db: Session) -> list[Conversation]:
    """
    Get all non-archived conversations where:
    - The most recent message is from an assistant
    - The last message was sent within the last 24 hours
    
    Returns:
        list[Conversation]: List of conversations meeting the criteria
    """
    # Calculate timestamp for 24 hours ago
    cutoff_time = datetime.now() - timedelta(hours=24)
    
    # Subquery to get the most recent message for each conversation
    latest_messages = (
        select(Message.conversation_id, 
               Message.role,
               Message.create_time)
        .distinct(Message.conversation_id)
        .order_by(Message.conversation_id, desc(Message.create_time))
        .subquery()
    )
    
    # Main query
    query = (
        select(Conversation)
        .join(latest_messages, Conversation.id == latest_messages.c.conversation_id)
        .where(and_(
            Conversation.archived == False,
            latest_messages.c.role == "assistant",
            latest_messages.c.create_time >= cutoff_time
        ))
    )
    
    return list(db.execute(query).scalars().all())


