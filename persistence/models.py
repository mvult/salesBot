from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from persistence.db import Base

class Agent(Base):
    __tablename__ = "agent"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    model = Column(String, nullable=False)
    identity = Column(String, nullable=False)
    instructions = Column(String, nullable=False)
    tools = Column(JSON)

class Conversation(Base):
    __tablename__ = "conversation"
    id = Column(Integer, primary_key=True, index=True)
    agentid = Column(Integer, ForeignKey("agent.id"), nullable=False)
    outcome = Column(String, nullable=True)
    platform = Column(String, nullable=True)
    create_time = Column(DateTime(timezone=True), default=func.now())
    handedOff = Column(Boolean, default=False)
    handOffTime = Column(DateTime(timezone=True), default=func.now())
    archived = Column(Boolean, default=False)
    client_id = Column(String)
    client_name = Column(String)

class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String, ForeignKey("conversation.id"), nullable=False)
    content = Column(String, nullable=False)
    role = Column(String, nullable=False) 
    source = Column(String, nullable=False)
    create_time = Column(DateTime(timezone=True), default=func.now())
    sender_id = Column(String, nullable=False)
    recipient_id = Column(String, nullable=False)
    bundle_id = Column(String)
