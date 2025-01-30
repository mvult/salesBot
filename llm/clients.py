import os
from anthropic import Anthropic

anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_KEY"))
