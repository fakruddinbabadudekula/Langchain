import streamlit as st
from backend import chatbot
import uuid
from langchain_core.messages import HumanMessage

# utils functions
def generate_id():
    thread_id = str(uuid.uuid4())
    return thread_id

def clean_chat_history():
    st.session_state['messages_history']=[]

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    # Check if messages key exists in state values, return empty list if not
    return state.values.get('messages', [])



# checking the if messages_history is exist if not create one with empty array
if 'messages_history' not in st.session_state:
    st.session_state['messages_history']=[]

if 'current_thread_id' not in st.session_state:
    st.session_state['current_thread_id']=generate_id()

if 'threads_history' not in st.session_state:
    st.session_state['threads_history']=[st.session_state['current_thread_id']]

st.sidebar.title("Chatbot")


if st.sidebar.button("New Chat"):
    new_id=generate_id()
    st.session_state['threads_history'].append(new_id)
    st.session_state['current_thread_id']=new_id
    clean_chat_history()


for thread in st.session_state['threads_history']:
    if st.sidebar.button(thread):
        clean_chat_history()
        st.session_state['current_thread_id']=thread
        messages=load_conversation(thread_id=thread)
        for message in messages:
            st.session_state['messages_history'].append(
                {
                    'role':'user' if isinstance(message, HumanMessage) else 'assistant',
                    'content':message.content
                }
            )


        


# Printing the all previous messages which are stored in the messages_history in session state
for message in st.session_state['messages_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# Configurable object to save and track the messages histroy
CONFIG = {'configurable': {'thread_id': st.session_state['current_thread_id']}}

user_input=st.chat_input()

# Executed when the user enters the input
if user_input:
    # adding the user input to message_history 
    st.session_state['messages_history'].append({'role':'user','content':user_input})

    # Printing the user message 
    with st.chat_message('user'):
        st.text(user_input)

   

    # Printing the assistant message
    with st.chat_message('assistant'):
    
    # Stream the assistant's reply into the chat UI
        response = st.write_stream(
        # Generator comprehension: extract only the content (text) 
        # from each streamed message chunk
        message_chunk.content 
        for message_chunk, metadata in chatbot.stream(
            
            # Input to the chatbot: one user message
            {'messages': [HumanMessage(content=user_input)]},
            
            # Config: thread_id keeps conversation state across turns
            config=CONFIG,
            
            # Stream mode: stream full messages instead of raw tokens
            stream_mode='messages'
        )
    )
        st.session_state['messages_history'].append({
        'role':'assistant',
        'content':response
    })