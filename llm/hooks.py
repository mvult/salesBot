from typing import cast, Literal
import logging

from anthropic.types.message_param import MessageParam
from anthropic.types.message import Message as AnthropicResponse

from config import SALES_BOT_MODE
from llm.handoff import get_handoff_message
from persistence.models import Message, Agent
from persistence.db import get_managed_db
from llm.clients import anthropic_client
from llm.backup import get_response_from_open_ai
from logs.setup import llm_logger


#Return is message, should_handoff, and should_skip_message
def generate_llm_message(messages: list[Message], agent_id: int, max_tokens: int = 512) -> tuple[str, bool, bool]:
    llm_logger.debug(f"Generating LLM message with {len(messages)} messages")
    if SALES_BOT_MODE != "live":
        llm_logger.debug("Skipping llm")
        return "Test message", False, False
    print(f"Getting to LLM with {len(messages)} messages")

    with get_managed_db() as db:
        agent = db.query(Agent).filter_by(id=agent_id).one()
    
    llm_messages: list[MessageParam] = [MessageParam(role=cast(Literal['user', 'assistant'], m.role), content= m.content) for m in messages]
    llm_messages: list[MessageParam] = [MessageParam(role="user", content= agent.instructions), MessageParam(role="assistant", content="Understood"), *llm_messages]
    
    try:
        response: AnthropicResponse = anthropic_client.messages.create(
            model=agent.model,
            system=agent.identity,
            max_tokens=max_tokens,
            messages=llm_messages,
            tools=agent.tools
        )  

        llm_logger.debug(f"Anthropic: {response}")

        if anthropic_error(response):
            return get_response_from_open_ai(messages, agent.identity, agent.instructions)
            # return "", True, True

        if asks_for_tool_use(response):
            return get_handoff_message(messages, agent.model), True, False

        if response.content[0].type == "text":
            print(f"Received LLM msg:\n ${response.content[0].text}\n--end--\n\n")
            return response.content[0].text, False, False
        else:
            raise Exception("An error occurred: Unexpected response type")
    except Exception as e:
        llm_logger.debug(f"Anthropic error: {e}")
        print("Anthropic error" , e)
        raise e


def anthropic_error(response: AnthropicResponse) -> bool:
    try:
        for c in response.content:
            if c.type == "error":
                return True
        return False
    except Exception:
        return True

def asks_for_tool_use(response: AnthropicResponse) -> bool:
    try:
        for c in response.content:
            if c.type == "tool_use":
                return True
        return False

    except Exception as e:
        print("Error in asks_for_tool_use", e)
        return False

