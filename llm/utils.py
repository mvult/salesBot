from persistence.models import Message

def summarize_conversation(msgs: list[Message]) -> str:
    """
    Summarize a conversation by concatenating all messages.
    
    Args:
        msgs: List of messages to summarize
        
    Returns:
        str: Concatenated conversation
    """
    ret = ""
    for msg in msgs:
        timestamp = msg.create_time.strftime("%Y-%m-%d %H:%M:%S")
        role_prefix = {
            "assistant": "Asistente de Ventas",
            "user": "Cliente",
            "system": "Sistema"
        }.get(msg.role, msg.role)
        
        ret += (f"[{timestamp}] {role_prefix}: {msg.content}\n")
    return ret
