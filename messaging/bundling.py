import uuid
import re

from nltk.tokenize import sent_tokenize

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

def split_llm_response(text: str) -> list[str]:
    sentences = sent_tokenize(text)
    ret = []
    current = ""

    for s in sentences:
        current += s + " "
        if len(current) > 160:
            ret.append(current.strip())
            current = ""
    if current != "": ret.append(current.strip())

    return ret
# def split_llm_response(text: str) -> list[str]:
#     # Split text into sentences
#     sentences = re.split(r'(?<=[.!?]) +', text)
#
#     messages = []
#     current_group = []
#
#     for sentence in sentences:
#         # Normalize whitespace and punctuation spacing
#         stripped = re.sub(r'([.!?])\s+', r'\1', sentence.strip())
#         if not stripped:
#             continue
#
#         # Handle long sentences
#         if len(stripped) > 160:
#             if current_group:
#                 messages.append(" ".join(current_group))
#                 current_group = []
#             messages.append(stripped)
#         else:
#             current_group.append(stripped)
#             if len(current_group) == 2:
#                 messages.append(" ".join(current_group))
#                 current_group = []
#
#     if current_group:
#         messages.append(" ".join(current_group))
#
#     return messages

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

    new_msgs.append(Message(content=current_content, role=current_role, bundle_id=current_bundle_id))

    return new_msgs






