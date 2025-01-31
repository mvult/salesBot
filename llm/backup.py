from typing import cast, Iterable

from openai.types.chat import ChatCompletionMessageParam 

from llm.clients import open_ai_client
from persistence.models import Message


def get_response_from_open_ai(messages: list[Message], system: str, first_message: str) -> tuple[str, bool, bool]:

    try:
        msgs = [
                {"role": "developer", "content": system},
                {"role": "user", "content": first_message},
                {"role": "assistant", "content": "Understood"}
        ]

        for m in messages:
            msgs.append({"role": m.role, "content": m.content})

        
        response = open_ai_client.chat.completions.create(
            model="gpt-4o",
            messages=cast(Iterable[ChatCompletionMessageParam], msgs))

        ret = response.choices[0].message.content
        if ret:
            return ret, False, False
        return "", True, True 
    except Exception as e:
        print("Error in get_response_from_open_ai", e)
        return "", True, True




