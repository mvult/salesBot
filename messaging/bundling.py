import uuid
import re

from persistence.models import Message

def add_bundle_info(msgs: list[Message])-> list[Message]:
    if not msgs:
        return msgs 

    current_bundle_id = None
    current_role = None

    for message in msgs:
        if message.bundle_id:
            # If the message already has a bundle_id, reset the current bundle and role
            current_bundle_id = None
            current_role = None
        else:
            if current_bundle_id is None or message.role != current_role:
                # Start a new bundle if no current bundle or role changes
                current_bundle_id = str(uuid.uuid4())
                current_role = message.role

            # Assign the current bundle_id to the message
            message.bundle_id = current_bundle_id

    return msgs


def split_llm_response(text: str, max_length: int = 160,  max_sentences: int = 4) -> list[str]:
   
    # Split text into sentences using regex (simple heuristic)
    sentences = re.split(r'(?<=[.!?]) +', text)  # Split on spaces after punctuation

    messages = []
    current_message = ""
    current_sentence_count = 0

    for sentence in sentences:
        # If adding the next sentence would exceed the max length or max sentences, finalize the current message
        if (len(current_message) + len(sentence) > max_length) or (current_sentence_count >= max_sentences):
            if current_message:
                messages.append(current_message.strip())
                current_message = ""
                current_sentence_count = 0

        # Add the sentence to the current message
        current_message += sentence + " "
        current_sentence_count += 1

    # Add the last message if it exists
    if current_message.strip():
        messages.append(current_message.strip())

    return messages


def bundle_messages(msgs: list[Message]) -> list[Message]:
    new_msgs = []
    current_bundle_id = None
    current_role = None
    current_content = ""

    for msg in msgs:
        assert msg.bundle_id, "All messages must have a bundle_id"

        if current_bundle_id is None:
            current_bundle_id = msg.bundle_id
            current_role = msg.role
            current_content = msg.content
            continue

        if current_bundle_id and current_bundle_id != msg.bundle_id:
            new_msgs.append(Message(content=current_content, role=current_role, bundle_id=current_bundle_id))
            current_bundle_id = msg.bundle_id
            current_role = msg.role
            current_content = msg.content
            continue

        current_content += " " + msg.content

    return new_msgs






