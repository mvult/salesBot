import os
import json

from anthropic import Anthropic, Response

# from config import IDENTITY, TOOLS, MODEL, get_quote
from config import SALES_BOT_MODE
from persistence.models import Message, Agent
from persistence.db import get_db

client = Anthropic(api_key=os.getenv("ANTHROPIC_KEY"))
HANDOFF_MESSAGE = "Es buena pregunta. No estoy 100% segura. Déjame preguntarle a mi jefe. Vuelvo en unos minutos."

def generate_llm_message(messages: list[Message], agent_id: int, max_tokens: int = 512) -> str:
    if SALES_BOT_MODE != "live":
        return "Test message"

    with get_db() as db:
        agent = db.query(Agent).filter_by(id=agent_id).first()
    
    llm_messages = [{"role": m.role, "content": m.content} for m in messages]
    llm_messages = [{"role": "user", "content": agent.instructions}, {"role": "assistant", "content": "Understood"}, *llm_messages]
    

    print("messages\n\n\n\n")
    print(messages)
    print(agent.tools)
    print(json.loads(agent.tools))
    try:
        response = client.messages.create(
            model=agent.model,
            system=agent.identity,
            max_tokens=max_tokens,
            messages=messages,
            tools=json.loads(agent.tools)
        )  
        print("response\n\n\n\n")
        print(response)
        if "error" in response:
            return f"An error occurred: {response['error']}"

        if asks_for_tool_use(response):
            return HANDOFF_MESSAGE

        if response.content[0].type == "text":
            return response.content[0].text
    
        else:
            raise Exception("An error occurred: Unexpected response type")
    except Exception as e:
        print("Anthropic error" , e)
        raise e



def asks_for_tool_use(response: Response) -> bool:
    try:
        for c in response.content:
            if c.type == "tool_use":
                return True
        return False

    except Exception as e:
        print("Error in asks_for_tool_use", e)
        return False


# def _generate_llm_message(messages, max_tokens=512) -> str:
#
#     messages[0]['content'] = [{'cache_control':{'type':'ephemeral'}, 'text': messages[0]['content'], 'type':'text'}]
#
#     print("messages\n\n\n\n")
#     print(messages)
#     try:
#         response = client.messages.create(
#             model=MODEL,
#             system=IDENTITY,
#             max_tokens=max_tokens,
#             messages=messages,
#         )  
#         print("response\n\n\n\n")
#         print(response)
#         if "error" in response:
#             return f"An error occurred: {response['error']}"
#
#         if response.content[0].type == "text":
#             return response.content[0].text
#             # return {"role": "assistant", "content": response_text}
#
#         else:
#             raise Exception("An error occurred: Unexpected response type")
#     except Exception as e:
#         print("error here" , e)
#         # return {"role":"assistant",'content':f"An error occurred {e}"}
#         raise e
#

