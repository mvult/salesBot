from typing import  List

from fastapi import FastAPI, HTTPException, Depends, Query, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.orm import Session

from persistence.models import Agent, Conversation, Message
from persistence.db import engine, get_db, Base
from pydanticModels import AgentCreateSchema, AgentSchema, ConversationPatchSchema, ConversationSchema, MessageSchema, WebhookPayloadSchema
from messaging.hooks import evaluate_conversation, receive_message_event
from config import WEBHOOK_TOKEN

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
    return db.execute(select(Agent)).scalars().all()
 

@app.get("/conversations", response_model=List[ConversationSchema])
def get_conversations(db: Session = Depends(get_db)):
    return db.query(Conversation).all()

@app.get("/conversations/{convo_id}", response_model=ConversationSchema)
def get_conversation(convo_id: int, db: Session = Depends(get_db)):
    return db.query(Conversation).filter_by(id=convo_id).first()

@app.patch("/conversations/{convo_id}", response_model=ConversationSchema)
def patch_conversation(convo_id: int, update: ConversationPatchSchema, db: Session = Depends(get_db)):
    update_data = update.model_dump(exclude_unset=True)
    update_dict = {getattr(Conversation, key): value for key, value in update_data.items()}

    db.query(Conversation).filter_by(id=convo_id).update(update_dict)
    db.commit()
    return db.query(Conversation).filter_by(id=convo_id).first()

@app.get("/conversations/{convo_id}/messages", response_model=List[MessageSchema])
def get_messages(convo_id: int, db: Session = Depends(get_db)):
    return db.query(Message).filter_by(conversation_id=convo_id).all()

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

@app.post("/webhooks")
def handle_webevent(event: WebhookPayloadSchema, background_tasks: BackgroundTasks):
    print("Pretty-printed Webhook event:")
    print(event.model_dump_json(indent=2))

    if event.object == "instagram" and event.entry[0].changes[0].field == "messages":
        convo = receive_message_event(event)
        background_tasks.add_task(evaluate_conversation, convo.id, convo.client_id)
        
    return {"message": "JSON received"}
