import pytest

from messaging.external import send_email_to_operators
from persistence.models import Conversation

@pytest.mark.external
def test_send_email():
    send_email_to_operators(Conversation(client_name="Test client", client_id="test_client_id"), "miguel@evenlift.io")
