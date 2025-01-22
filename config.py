import os
from dotenv import load_dotenv

load_dotenv()

IG_ACCESS_TOKEN=os.getenv('IG_ACCESS_TOKEN')
WEBHOOK_TOKEN=os.getenv('WEBHOOK_TOKEN')
EVENLIFT_IG_ID=os.getenv('EVENLIFT_IG_ID')
SALES_BOT_MODE=os.getenv('SALES_BOT_MODE')

