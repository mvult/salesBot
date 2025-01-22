import random

from sqlalchemy import func
from sqlalchemy.orm import Session 
from sqlalchemy.sql import text

from persistence.models import Agent 


# Exploration rate
EPSILON = 0.2

class LocalAgent:
    id: int
    conversations: int
    successes: int

def get_optimized_agent(session: Session) -> Agent:
    if random.random() < EPSILON:
        return session.query(Agent).order_by(func.random()).one()
    
    results = session.execute(text("""
        SELECT agent_id,
               COUNT(*) AS total_conversations,
               SUM(CASE WHEN outcome = 'success' THEN 1 ELSE 0 END) AS successes
        FROM conversation
        GROUP BY agent_id
        """)).fetchall()


    if len(results) == 0:
        print("No agents with conversations found, selecting randomly")
        return session.query(Agent).order_by(func.random()).one()

    agents_with_rates = [
        (row.agent_id, row.successes / row.total_conversations) for row in results
    ]

    max_rate = max(rate for _, rate in agents_with_rates)
    
    # Get all agents with max rate
    best_agents = [agent_id for agent_id, rate in agents_with_rates if rate == max_rate]
    
    # Random choice if multiple
    best_agent_id = random.choice(best_agents)

    return session.query(Agent).filter(Agent.id == best_agent_id).one()



