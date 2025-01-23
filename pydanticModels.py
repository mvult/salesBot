from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Any

# Pydantic models for Agent
class AgentBaseSchema(BaseModel):
    name: str
    instructions: str
    model: str
    identity: str
    tools: Any

class AgentCreateSchema(AgentBaseSchema):
    pass

class AgentSchema(AgentBaseSchema):
    id: int

    class Config:
        from_attributes = True  # Enable ORM mode

# Pydantic models for Conversation
class ConversationBaseSchema(BaseModel):
    agent_id: int
    outcome: Optional[str] = None
    platform: Optional[str] = None
    handed_off: Optional[bool] = False
    hand_off_time: Optional[datetime] = None

class ConversationCreateSchema(ConversationBaseSchema):
    pass

class ConversationPatchSchema(BaseModel):
    outcome: Optional[str] = None
    handed_off: Optional[bool] = None
    archived: Optional[bool] = None

class ConversationSchema(ConversationBaseSchema):
    id: int

    class Config:
        from_attributes = True  # Enable ORM mode


# Pydantic models for Message
class MessageBaseSchema(BaseModel):
    content: Optional[str] = None
    role: Optional[str] = None
    source: Optional[str] = None
    create_time: Optional[datetime] = None
    bundle_id: Optional[str] = None

class MessageCreateSchema(MessageBaseSchema):
    pass

class MessageSchema(MessageBaseSchema):
    id: int
    conversation_id: int

    class Config:
        from_attributes = True
    

# Define models for the nested structures
class Sender(BaseModel):
    id: str

class Recipient(BaseModel):
    id: str

class Message(BaseModel):
    mid: str
    text: str

class Reaction(BaseModel):
    mid: str
    action: str
    reaction: str
    emoji: str

class Read(BaseModel):
    mid: int

# This is where the different events differ in structure.  message vs. reaction vs read
class Value(BaseModel):
    sender: Sender
    recipient: Recipient
    timestamp: str
    message: Optional[Message] = None
    reaction: Optional[Reaction] = None
    read: Optional[Read] = None

class Change(BaseModel):
    field: str
    value: Value

class Entry(BaseModel):
    id: str
    time: int
    changes: List[Change]

class WebhookPayloadSchema(BaseModel):
    entry: List[Entry]
    object: str
