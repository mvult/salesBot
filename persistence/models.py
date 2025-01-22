from datetime import datetime

from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

from persistence.db import Base

class Agent(Base):
    __tablename__ = "agent"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    model: Mapped[str] = mapped_column(String, nullable=False)
    identity: Mapped[str] = mapped_column(String, nullable=False)
    instructions: Mapped[str] = mapped_column(String, nullable=False)
    call_link: Mapped[str] = mapped_column(String, nullable=True)
    tools: Mapped[dict] = mapped_column(JSON)

class Conversation(Base):
    __tablename__ = "conversation"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    agent_id: Mapped[int] = mapped_column(ForeignKey("agent.id"), nullable=False)
    outcome: Mapped[str | None] = mapped_column(String, nullable=True)
    platform: Mapped[str | None] = mapped_column(String, nullable=True)
    create_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    handed_off: Mapped[bool] = mapped_column(Boolean, default=False)
    hand_off_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    archived: Mapped[bool] = mapped_column(Boolean, default=False)
    client_id: Mapped[str] = mapped_column(String)
    client_name: Mapped[str] = mapped_column(String, nullable=True)

    # messages: Mapped[list["Message"]] = relationship(back_populates="conversation")


class Message(Base):
    __tablename__ = "message"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    conversation_id: Mapped[str] = mapped_column(ForeignKey("conversation.id"), nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    create_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    sender_id: Mapped[str] = mapped_column(String, nullable=False)
    recipient_id: Mapped[str] = mapped_column(String, nullable=False)
    bundle_id: Mapped[str | None] = mapped_column(String)
