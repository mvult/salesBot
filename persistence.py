from supabase import create_client, Client
from typing import List, Dict


class ConversationPersistence:
    def __init__(self, client):
        self.supabase = client
        self.table_name = "conversations"

    def add_message(self, conversation_name: str, role: str, message: str):
        data = {
            "name": conversation_name,
            "role": role,
            "content": message,
        }
        response = self.supabase.table(self.table_name).insert(data).execute()
        if 'error' in response:
            raise Exception(f"Error inserting message: {response.error.message}")

    def get_conversation(self, conversation_name: str) -> List[Dict[str, str]]:
        response = self.supabase.table(self.table_name).select("role, content").eq("name", conversation_name).order("created_at", desc=True).execute()

        if 'error' in response:
            raise Exception(f"Error fetching conversation: {response.error.message}")
        return response.data

    def list_conversations(self) -> List[str]:
        response = self.supabase.table("conversations").select("name").execute()
        if 'error' in response:
            raise Exception(f"Error listing conversations: {response.error.message}")
        return list(set([row["name"] for row in response.data]))

    def delete_conversation(self, conversation_name: str):
        """
        Deletes an entire conversation by name.
        :param conversation_name: The name of the conversation to delete.
        """
        response = self.supabase.table(self.table_name).delete().eq("name", conversation_name).execute()
        if 'error' in response:
            raise Exception(f"Error deleting conversation: {response.error.message}")


