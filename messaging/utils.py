from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

from persistence.models import Conversation
from external import send_email_to_operators


def calculate_typing_delay_seconds(message: str) -> float:
    num_chars = len(message) / 1.5
    total_delay = (num_chars * 0.1) + ((num_chars - 1) // 20 * 0.5)
    print(f"Delay for {len(message)} chars: {total_delay}")
    return total_delay  # Returns delay in seconds

async def handoff(convo: Conversation, db: AsyncSession):
    convo.handed_off = True
    await db.commit()
    send_email_to_operators(cast(Conversation, convo))
