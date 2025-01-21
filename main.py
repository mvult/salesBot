from datetime import datetime
from typing import Optional, List
import json

from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from persistence.models import Agent, Conversation, Message
from persistence.db import engine, get_db, Base
from pydanticModels import AgentCreateSchema, AgentSchema, ConversationCreateSchema, ConversationSchema, MessageCreateSchema, MessageSchema

WEBHOOK_TOKEN = "d90293nv0902m0wdmcmmksppldjkfs"

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/agents", response_model=AgentSchema)
def create_agent(agent: AgentCreateSchema, db: Session = Depends(get_db)):
    db_agent = Agent(**agent.dict())
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

@app.get("/agents", response_model=List[AgentSchema])
def get_agents(db: Session = Depends(get_db)):
    return db.query(Agent).all()

@app.post("/webhooks")
def handle_webevent(data: dict):
    print("Received JSON data:", data)

    # Optionally, pretty-print the JSON
    print("Pretty-printed JSON:")
    print(json.dumps(data, indent=2))

    return {"message": "JSON received", "data": data}

@app.get("/webhooks")
def verify_subscription(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_challenge: str = Query(..., alias="hub.challenge"),
    hub_verify_token: str = Query(..., alias="hub.verify_token"),
):
    print("In verification")

    if hub_verify_token == WEBHOOK_TOKEN and hub_mode == "subscribe":
        print("sending back")
        return hub_challenge 
    else:
        return HTTPException(status_code=403, detail="Invalid verify token")
