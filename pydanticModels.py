from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Pydantic models for Agent
class AgentBaseSchema(BaseModel):
    name: str
    instructions: str

class AgentCreateSchema(AgentBaseSchema):
    pass

class AgentSchema(AgentBaseSchema):
    id: int

    class Config:
        from_attributes = True  # Enable ORM mode

# Pydantic models for Conversation
class ConversationBaseSchema(BaseModel):
    agentid: int
    outcome: Optional[str] = None
    platform: Optional[str] = None
    handedOff: Optional[bool] = False
    handOffTime: Optional[datetime] = None

class ConversationCreateSchema(ConversationBaseSchema):
    pass

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

class MessageCreateSchema(MessageBaseSchema):
    pass

class MessageSchema(MessageBaseSchema):
    id: int
    conversation_id: int

    class Config:
        from_attributes = True
    
