import logging 
import os
from datetime import datetime
from zoneinfo import ZoneInfo



logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %Z',
    level=logging.INFO
)

logging.Formatter.converter = lambda *args: datetime.now(ZoneInfo("America/Mexico_City")).timetuple()

logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

## Webhook logger
webhook_logger = logging.getLogger("webhook_logger")
webhook_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(os.path.join(os.path.dirname(__file__), "webhook.log"), mode="a")
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
webhook_logger.addHandler(file_handler)

## errors logger
errors_logger = logging.getLogger("errors_logger")
errors_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(os.path.join(os.path.dirname(__file__), "errors.log"), mode="a")
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
errors_logger.addHandler(file_handler)

## LLM Logger
llm_logger = logging.getLogger("llm_responses")
llm_logger.setLevel(logging.DEBUG)
# file_handler = logging.FileHandler("llm_responses.log")
file_handler = logging.FileHandler(os.path.join(os.path.dirname(__file__), "llm_responses.log"), mode="a")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
llm_logger.addHandler(file_handler)

## Process Logger
process_logger = logging.getLogger("process")
process_logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(os.path.join(os.path.dirname(__file__), "process.log"), mode="a")
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
process_logger.addHandler(file_handler)
