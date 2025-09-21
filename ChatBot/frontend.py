import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage

# checking the if messages_history is exist if not create one with empty array
if 'messages_history' not in st.session_state:
    st.session_state['messages_history']=[]


# Printing the all previous messages which are stored in the messages_history in session state
for message in st.session_state['messages_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

# Configurable object to save and track the messages histroy
CONFIG = {'configurable': {'thread_id': 'thread-1'}}

user_input=st.chat_input()

# Executed when the user enters the input
if user_input:
    # adding the user input to message_history 
    st.session_state['messages_history'].append({'role':'user','content':user_input})

    # Printing the user message 
    with st.chat_message('user'):
        st.text(user_input)

    # invoke the graph and return the list of messages_history 
    response=chatbot.invoke({
        'messages':HumanMessage(content=user_input)
    },config=CONFIG)


    # adding the response to message_history
    st.session_state['messages_history'].append({
        'role':'assistant',
        'content':response['messages'][-1].content
    })

    # Printing the assistant message
    with st.chat_message('assistant'):
        st.text(response['messages'][-1].content)