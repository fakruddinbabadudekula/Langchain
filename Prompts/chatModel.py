from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from os import getenv
from dotenv import load_dotenv
load_dotenv()
model=ChatOpenAI(base_url=getenv("OPENROUTER_BASE_URL"),api_key=getenv("OPENROUTER_API_KEY"), model=getenv("OPENROUTER_MODEL"), temperature=0.7)

promt=ChatPromptTemplate(
    messages=[
        ("system", "You are a helpful coding assistant who helps users with Python code.And only returns code snippets.And the below are the previous messages in the chat history.According to the chat history, generate a code snippet that solves the problem."),
        MessagesPlaceholder("chat_history"),
    
    ],
    input_variables=["chat_history"]
)
chat_history = []
while True:
    question =input("You:Enter your question (or type 'exit' to quit): ")
    if question.lower() == 'exit':
        break
    chat_history.append(HumanMessage(content=question))
    prompt_input = promt.invoke({"chat_history": chat_history})
    response = model.invoke(prompt_input)
    chat_history.append(AIMessage(content=response.content))
    print("Assistant:", response.content)


print("\nChat History:")
print(chat_history)