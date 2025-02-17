from typing import  List, Optional
import asyncio
import traceback

from fastapi import FastAPI, HTTPException, Depends, Query, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from persistence.models import Agent, Conversation, Message
from persistence.db import engine, get_db, Base, get_managed_db
from pydanticModels import AgentBaseSchema, AgentCreateSchema, AgentSchema, ConversationPatchSchema, ConversationSchema, MessageSchema, IGMessagePayloadSchema
from messaging.hooks import evaluate_conversation, handle_message_from_evenlift, receive_message_event
from outbound.hooks import send_reactivation_outbound
from config import WEBHOOK_TOKEN, EVENLIFT_IG_ID
from logs.setup import webhook_logger, errors_logger

app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")
app.mount("/front", StaticFiles(directory="frontend/dist", html=True), name="root")

# @app.middleware("http")
# async def log_exceptions_middleware(request: Request, call_next):
#      try:
#          response = await call_next(request)
#          return response
#      except Exception as e:
#          tb = traceback.format_exc()
#          errors_logger.error(e)
#          errors_logger.error(tb)
#          # raise e
#          return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
#
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    errors_logger.error(
        f"Unhandled Exception: {str(exc)}",
        exc_info=True,  # Include stack trace
        extra={"path": request.url.path, "method": request.method},
    )
    return JSONResponse(
        content={"detail": "Internal Server Error"},
        status_code=500,
    )
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
        return [db.execute(select(Conversation).filter_by(client_id=client_id).order_by(desc(Conversation.most_recent_user_message))).scalars().first()]
    return db.query(Conversation).order_by(desc(Conversation.most_recent_user_message)).all()

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

        if event.object == "instagram" and event.get_sender_id() == EVENLIFT_IG_ID:
            with get_managed_db() as session:
                handle_message_from_evenlift(event, session)

    except Exception as e:
        print("Webhook error", e)
        print(f'Unexpected webhook.  Raw JSON below\n{raw_json}\n') 
        raise HTTPException(status_code=422, detail=f"Unprocessable entity: {e}")

    return {"message": "JSON received"}

@app.get("/simulateOutbound")
def handle_outbound(db: Session = Depends(get_db)):
    send_reactivation_outbound(db)
    return {"message": "Outreach simulated"}

