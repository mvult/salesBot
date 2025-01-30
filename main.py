from typing import  List, Optional
import logging
import os
import asyncio

from fastapi import FastAPI, HTTPException, Depends, Query, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from persistence.models import Agent, Conversation, Message
from persistence.db import engine, get_db, Base, get_managed_db
from pydanticModels import AgentBaseSchema, AgentCreateSchema, AgentSchema, ConversationPatchSchema, ConversationSchema, MessageSchema, IGMessagePayloadSchema
from messaging.hooks import evaluate_conversation, receive_message_event
from outbound.hooks import send_reactivation_outbound
from config import WEBHOOK_TOKEN, EVENLIFT_IG_ID

app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)

webhook_logger = logging.getLogger("webhook_logger")
webhook_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("webhook.log", mode="a")
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
webhook_logger.addHandler(file_handler)

logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
Base.metadata.create_all(bind=engine)

app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")
app.mount("/front", StaticFiles(directory="frontend/dist", html=True), name="root")

@app.post("/agents", response_model=AgentSchema)
def create_agent(agent: AgentCreateSchema, db: Session = Depends(get_db)):
    db_agent = Agent(**agent.model_dump())
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

@app.get("/agents", response_model=List[AgentSchema])
def get_agents(db: Session = Depends(get_db)):
    return db.execute(select(Agent)).scalars().all()

@app.patch("/agents/{agent_id}", response_model=AgentSchema)
def patch_agent(agent_id: int, update: AgentBaseSchema, db: Session = Depends(get_db)):
    update_data = update.model_dump(exclude_unset=True)
    update_dict = {getattr(Agent, key): value for key, value in update_data.items()}

    db.query(Agent).filter_by(id=agent_id).update(update_dict)
    db.commit()
    return db.query(Agent).filter_by(id=agent_id).first()

@app.delete("/agents/{agent_id}")
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter_by(id=agent_id).first()
    db.delete(agent)
    db.commit()
    return 


@app.get("/conversations", response_model=List[ConversationSchema])
def get_conversations(db: Session = Depends(get_db), client_id: Optional[str] = Query(None)):
    if client_id: 
        return [db.execute(select(Conversation).filter_by(client_id=client_id)).scalars().first()]
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

@app.delete("/conversations/{convo_id}")
def delete_conversation(convo_id: int, db: Session = Depends(get_db)):
    agent = db.query(Conversation).filter_by(id=convo_id).first()
    db.delete(agent)
    db.commit()
    return 

@app.get("/conversations/{convo_id}/messages", response_model=List[MessageSchema])
def get_messages(convo_id: int, db: Session = Depends(get_db)):
    msgs = db.execute(select(Message).filter_by(conversation_id=convo_id)).scalars().all()
    return msgs

@app.get("/webhooks")
def verify_subscription(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_challenge: str = Query(..., alias="hub.challenge"),
    hub_verify_token: str = Query(..., alias="hub.verify_token"),
):
    if hub_verify_token == WEBHOOK_TOKEN and hub_mode == "subscribe":
        print("sending back")
        return hub_challenge 
    else:
        return HTTPException(status_code=403, detail="Invalid verify token")

@app.post("/webhooks")
def handle_webevent(_event: Request, background_tasks: BackgroundTasks):
    raw_json = asyncio.run(_event.json())
    try:
        event= IGMessagePayloadSchema.model_validate(raw_json)
        print("Pretty-printed Webhook event:")
        print(event.model_dump_json(indent=2))
        webhook_logger.info(event.model_dump_json())

        if event.object == "instagram" and event.get_recipient_id() == EVENLIFT_IG_ID:
            with get_managed_db() as session:
                convo = receive_message_event(event, session)
                background_tasks.add_task(evaluate_conversation, convo.id, convo.client_id)
    except Exception as e:
        print("Webhook error", e)
        print(f'Unexpected webhook.  Raw JSON below\n{raw_json}\n') 
        raise HTTPException(status_code=422, detail=f"Unprocessable entity: {e}")

    return {"message": "JSON received"}

@app.get("/simulateOutbound")
def handle_outbound(db: Session = Depends(get_db)):
    send_reactivation_outbound(db)
    return {"message": "Outreach simulated"}

# @app.post("/webhooks")
# def handle_webevent(event: Request):
#     print(event)
#     try:
#         json_body = asyncio.run(event.json())
#         result = WebhookPayloadSchema.model_validate_json(json_body)
#         print("Valid", result)
#     except Exception as e:
#         print(e)
#
#     return {"message": "JSON received"}
