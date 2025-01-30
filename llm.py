import os
from typing import cast, Literal
import logging

from anthropic import Anthropic
from anthropic.types.message_param import MessageParam
from anthropic.types.message import Message as AnthropicResponse

from config import SALES_BOT_MODE
from persistence.models import Message, Agent
from persistence.db import get_managed_db

client = Anthropic(api_key=os.getenv("ANTHROPIC_KEY"))
HANDOFF_MESSAGE = "Es buena pregunta. No estoy 100% segura. Déjame preguntarle a mi jefe. Vuelvo en unos minutos."

llm_logger = logging.getLogger("llm_responses")
llm_logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("llm_responses.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
llm_logger.addHandler(file_handler)

def generate_llm_message(messages: list[Message], agent_id: int, max_tokens: int = 512) -> str:
    if SALES_BOT_MODE != "live":
        print("Skipping llm")
        return "Test message"
    print(f"Getting to LLM with {len(messages)} messages")

    with get_managed_db() as db:
        agent = db.query(Agent).filter_by(id=agent_id).one()
    
    llm_messages: list[MessageParam] = [MessageParam(role=cast(Literal['user', 'assistant'], m.role), content= m.content) for m in messages]
    llm_messages: list[MessageParam] = [MessageParam(role="user", content= agent.instructions), MessageParam(role="assistant", content="Understood"), *llm_messages]
    

    try:
        response: AnthropicResponse = client.messages.create(
            model=agent.model,
            system=agent.identity,
            max_tokens=max_tokens,
            messages=llm_messages,
            tools=agent.tools
        )  

        print("LLM RESPONSE\n\n", response)
        llm_logger.debug(response)
        if asks_for_tool_use(response):
            return HANDOFF_MESSAGE

        if response.content[0].type == "text":
            print(f"Received LLM msg:\n ${response.content[0].text}\n--end--\n\n")
            return response.content[0].text
        else:
            raise Exception("An error occurred: Unexpected response type")
    except Exception as e:
        print("Anthropic error" , e)
        raise e



def asks_for_tool_use(response: AnthropicResponse) -> bool:
    try:
        for c in response.content:
            if c.type == "tool_use":
                return True
        return False

    except Exception as e:
        print("Error in asks_for_tool_use", e)
        return False


