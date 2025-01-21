from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Agent(BaseModel):
    id: Optional[int] = None  # Auto-generated, optional for creation
    name: str
    desc: str
    instructions: str

    class Config:
        from_attributes = True  # Enable ORM mode


class Conversation(BaseModel):
    id: Optional[int] = None  # Auto-generated, optional for creation
    agentid: int
    outcome: Optional[str] = None
    platform: Optional[str] = None
    handedOff: Optional[bool] = False
    handOffTime: Optional[datetime] = None

    class Config:
        from_attributes = True  # Enable ORM mode


class Message(BaseModel):
    id: Optional[int] = None  # Auto-generated, optional for creation
    conversation_id: int
    content: str
    role: str
    source: Optional[str] = None
    create_time: Optional[datetime] = None

    class Config:
        from_attributes = True  # Enable ORM mode
