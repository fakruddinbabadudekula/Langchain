from langchain.prompts import PromptTemplate,ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
# Template for generating a response based on a given question and context
prompt_template = PromptTemplate(
    template="Given the question: {question} and the context: {context}, provide a detailed answer.",
    input_variables=["question", "context"]
)
print(prompt_template.invoke({'question':"What is LangChain?", 
                              'context':"LangChain is a framework for developing applications powered by language models."}))
print("\n")
# Template for a chat interaction with a system message and user input
chat_template = ChatPromptTemplate(
    messages=[
        ("system", "You are a helpful assistant."),
        ("user", "{question}"),
        ("assistant", "Sure, I can help with that. {context}")
    ],
    input_variables=["question", "context"]
)
print(chat_template.invoke({'question':"What is LangChain?","context":"LangChain is a framework for developing applications powered by language models."}))

print("\n")

placeholder= ChatPromptTemplate(
    [('system',"You are a helpful assistant."),
    MessagesPlaceholder("chat_history"),
    ('user', "{question}"),]
)

print(placeholder.invoke({'question':"What is LangChain?",
                          'chat_history':["What is LangChain?\nAssistant: LangChain is a framework for developing applications powered by language models.","What is LangChain?\nAssistant: LangChain is a framework for developing applications powered by language models."]}))#Here the two messages in chat history are by default taken as user messages until we specify otherwise.


print(placeholder.invoke({'question':"What is LangChain?",
                          'chat_history':[HumanMessage(content="What is LangChain?\nAssistant: LangChain is a framework for developing applications powered by language models."),AIMessage(content="What is LangChain?\nAssistant: LangChain is a framework for developing applications powered by language models.")]}).messages)#
