import os
from anthropic import Anthropic
from openai import OpenAI

anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_KEY"))
open_ai_client = OpenAI() 
