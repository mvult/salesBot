from anthropic import Anthropic
from config import IDENTITY, TOOLS, MODEL, get_quote
import streamlit as st
# from dotenv import load_dotenv
#
# load_dotenv()

# client = Anthropic(api_key=anthropic_key)
client = Anthropic(api_key=st.secrets['anthropic_key'])

def generate_message(messages, max_tokens=512):
    
    messages[0]['content'] = [{'cache_control':{'type':'ephemeral'}, 'text': messages[0]['content'], 'type':'text'}]

    print("messages\n\n\n\n")
    print(messages)
    try:
        response = client.messages.create(
            model=MODEL,
            system=IDENTITY,
            max_tokens=max_tokens,
            messages=messages,
            tools=TOOLS,
        )  
        print("response\n\n\n\n")
        print(response)
        if "error" in response:
            return f"An error occurred: {response['error']}"

        if response.content[0].type == "text":
            response_text = response.content[0].text
            return {"role": "assistant", "content": response_text}
    
        else:
            raise Exception("An error occurred: Unexpected response type")
    except Exception as e:
        print("error here" , e)
        return {"role":"assistant",'content':f"An error occurred {e}"}


