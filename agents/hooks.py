import random

from sqlalchemy import func, Integer, Session

from persistence.models import Agent, Conversation
from persistence.db import get_db

# Exploration rate
EPSILON = 0.2

def get_optimized_agent(session: Session) -> Agent:
    if random.random() < 0.2:
        return Agent.query.order_by(func.random()).first()
    
    (best_agent, success_rate) = (
    session.query(Agent, func.avg((Conversation.outcome == 'success').cast(Integer)).label('success_rate'))
    .join(Conversation, Agent.id == Conversation.agent_id)
    .group_by(Agent.id)
    .order_by(func.avg((Conversation.outcome == 'success').cast(Integer)).desc())
    .first()
    )

    print("Success rate " + success_rate)
    return best_agent

