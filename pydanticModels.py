from datetime import datetime
from typing import Optional, List, Any, Literal, cast
import json

from pydantic import BaseModel, Json, field_validator, ValidationError

# Pydantic models for Agent
class AgentBaseSchema(BaseModel):
    name: str
    instructions: str
    model: Literal["claude-3-5-sonnet-latest"] 
    identity: str
    tools: Any

    @field_validator('tools')
    def validate_json(cls, value):
        if isinstance(value, str):
            value = json.loads(value)

        assert isinstance(value, (list))
        assert len(value) == 0 or isinstance(value[0], dict)
        return value 

class AgentCreateSchema(AgentBaseSchema):
    pass

class AgentSchema(AgentBaseSchema):
    id: int

    class Config:
        from_attributes = True  # Enable ORM mode

# Pydantic models for Conversation
class ConversationBaseSchema(BaseModel):
    agent_id: int
    client_id: str
    outcome: Optional[str] = None
    platform: Optional[str] = None
    handed_off: Optional[bool] = False
    hand_off_time: Optional[datetime] = None
    archived: Optional[bool] = False
    most_recent_user_message: Optional[datetime] = None

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
    
# IGMessagePayloadSchema
class Sender(BaseModel):
    id: str

class Recipient(BaseModel):
    id: str

# This is where the different events differ in structure.  message vs. reaction vs read
class WebhookMessage(BaseModel):
    mid: str
    text: Optional[str] = None
    attachments: Optional[Any] = None

class MessagingEntry(BaseModel):
    message: WebhookMessage
    recipient: Recipient 
    sender: Sender
    timestamp: int

class Entry(BaseModel):
    id: str
    time: int
    messaging: List[MessagingEntry]

class IGMessagePayloadSchema(BaseModel):
    entry: List[Entry]
    object: str

    def has_attachment(self) -> bool:
        if self.entry[0].messaging[0].message.attachments is not None:
            return True
        return False

    def get_text_content(self) -> str:
        if self.entry[0].messaging[0].message.attachments is not None:
            return "<Message was an attachment>"
        return cast(str, self.entry[0].messaging[0].message.text)
    
    def get_sender_id(self) ->str:
        return self.entry[0].messaging[0].sender.id

    def get_recipient_id(self) ->str:
        return self.entry[0].messaging[0].recipient.id
