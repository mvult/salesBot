from config import IDENTITY, COMMON_QUESTIONS, EXAMPLES, ADDITIONAL_GUARDRAILS
import streamlit as st
from chatbot import generate_message
from persistence import  ConversationPersistence
from supabase import create_client

TASK_INSTRUCTIONS = ' '.join([COMMON_QUESTIONS, EXAMPLES, ADDITIONAL_GUARDRAILS])

persistence = ConversationPersistence(create_client(st.secrets['SUPABASE_URL'], st.secrets['SUPABASE_KEY']))

def switch_conversation(name):
    st.session_state.current_conversation = name

def add_conversation():
    if st.session_state.new_conversation:
        name = st.session_state.new_conversation
        persistence.add_message(name, "user", TASK_INSTRUCTIONS)
        persistence.add_message(name, "assistant", "Understood")
        st.session_state.new_conversation = ""  
        switch_conversation(name)

def main():
    conversations = persistence.list_conversations()
    
    if 'current_conversation' in st.session_state:
        st.title(st.session_state.current_conversation)
        messages = persistence.get_conversation(st.session_state.current_conversation)
        
        for message in messages[2:]:
            with st.chat_message(message['role']):
                st.markdown(message['content'])
      

        if user_msg := st.chat_input("Type your message here..."):
            persistence.add_message(st.session_state.current_conversation, "user", user_msg)
            st.chat_message("user").markdown(user_msg)
            messages.append({'role':"user", "content": user_msg})

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response_placeholder = st.empty()
                    full_response = generate_message(messages)
                    persistence.add_message(st.session_state.current_conversation, "assistant", full_response['content'])
                    response_placeholder.markdown(full_response['content'])

    else:
        st.title("Select conversation...")

    st.sidebar.header("Conversations")
    selected_conversation = st.sidebar.selectbox(
        "Select Conversation",
        options=conversations,
        key="current_conversation",
        on_change=lambda: switch_conversation(st.session_state.current_conversation),
    )

    st.sidebar.text_input("New Conversation Name", key="new_conversation")

    st.sidebar.button("Add Conversation", on_click=add_conversation)

    if st.sidebar.button("Delete Conversation"):
        persistence.delete_conversation(st.session_state.current_conversation)
        conversations = [x for x in conversations if x != st.session_state.current_conversation]

    print(st.session_state)

if __name__ == "__main__": main()





