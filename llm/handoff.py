from typing import cast
import json

from anthropic.types.message_param import MessageParam
from anthropic.types.message import Message as AnthropicResponse

from persistence.models import Message
from llm.clients import anthropic_client
from llm.utils import summarize_conversation

DEFAULT_HANDOFF_MESSAGE = "No estoy 100% segura. Déjame preguntarle a mi jefe. Vuelvo en unos minutos."
DEFAULT_HANDOFF_IDENTITY = """Eres un coach de ventas."""

def get_handoff_message(msgs: list[Message], model: str) -> str:
    try:
        prompt = build_handoff_prompt(msgs)
        response: AnthropicResponse = anthropic_client.messages.create(
            model=model,
            system=DEFAULT_HANDOFF_IDENTITY,
            max_tokens=500,
            messages=[MessageParam(role="user", content=prompt)],
        )  

        print("HANDOFF LLM RESPONSE\n\n", response)

        if response.content[0].type == "text":
            print(f"Received LLM msg:\n ${response.content[0].text}\n--end--\n\n")
            raw_res = response.content[0].text
            parsed = json.loads(raw_res)
            return parsed['response']

        else:
            raise Exception("An error occurred: Unexpected response type")
    
    except Exception as e:
        print("handoff error", e)
        raise e
        return DEFAULT_HANDOFF_MESSAGE




def build_handoff_prompt(msgs: list[Message]) -> str:
    conversation_parts = []
    
    instruction = """Por favor, lee detenidamente la siguiente conversación de ventas.
Tu tarea es encontrar una razon razonable para communicar un 'hand-off' a tu gerente.  For ejemplo:
- Si la conversación termina en el usuario diciendo que los horarios disponibles no funcionan para el, reponde algo como "Te pido disculpas, lamento mucho que no hay horarios convenientes.  Dejame checar con mi jefe ver que se puede hacer.  Dame unos minutos."
- Si el usuario busca informacion, responde algo como "No estoy segura de eso.  Dejame preguntarle a mi jefe.  Vuelvo en unos minutos."

No te pases de 1-2 frases.  Alguien mas va continuar la conversasion.  Siempre se amable y alegre.  

Responde con un JSON que tenga el siguiente formato:
{
    "response": string  //el texto que debemos utilizar para responderle al cliente 
}

La conversasion es la siguiente:
"""
    conversation_parts.append(instruction)
    
    # Format each message with role and timestamp
    summarized_convo = summarize_conversation(cast(list, msgs))
    conversation_parts.append(summarized_convo)
    
    # Join all parts with double newlines for clarity
    return "\n\n".join(conversation_parts)
