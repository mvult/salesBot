from datetime import datetime
from typing import cast

from sqlalchemy import select
from sqlalchemy.orm import Session

from persistence.models import Conversation, Message
from llm.utils import summarize_conversation

def build_conversation_prompt(db: Session, conversation: Conversation) -> str:
    """
    Builds a formatted conversation history with a Spanish prompt for the LLM.
    
    Args:
        db: Database session
        conversation: Conversation to format
        
    Returns:
        str: Formatted conversation with prompt
    """
    # Get all messages for this conversation ordered by creation time
    messages = db.execute(
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.create_time)
    ).scalars().all()
    
    # Build the conversation history
    conversation_parts = []
    
    # Add Spanish instruction prompt
    instruction = """Por favor, lee detenidamente la siguiente conversación de ventas.
Tu tarea es:
1. Determinar si es apropiado continuar la conversación de ventas
2. Si es apropiado, proponer un mensaje para continuar la conversación

Responde con un JSON que tenga el siguiente formato:
{
    "should_respond": boolean,  // true si debemos continuar, false si no
    "response": string  // mensaje sugerido si should_respond es true, explicación si es false
}

La conversación es la siguiente:
"""
    conversation_parts.append(instruction)
    
    # Format each message with role and timestamp
    summarized_convo = summarize_conversation(cast(list, messages))
    conversation_parts.append(summarized_convo)
    
    # Join all parts with double newlines for clarity
    return "\n\n".join(conversation_parts)


