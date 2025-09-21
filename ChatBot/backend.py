from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph,END,START,add_messages
from typing import TypedDict,Annotated,List
from pydantic import BaseModel
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
# 2. Initialize Gemini 2.5 Pro
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0.7,
)

# Creating the checkpointer object using InMEmorySaver()
checkpointer=InMemorySaver()

# Graph state and messages values stores the list of basemessage objects like aimessage,humanmessage etc
class State(TypedDict):
    messages:Annotated[List[BaseMessage],add_messages]

# llm_node which is taking hte user input and perform the llm task and gives the response
def llm_node(state:State):
    messages=state['messages']
    response=llm.invoke(messages)
    return {
        'messages':response
    }

# Creating the graph with llm_node
graph=StateGraph(state_schema=State)

graph.add_node('llm_node',llm_node)

graph.add_edge(START,'llm_node')
graph.add_edge('llm_node',END)

# compiling the graph and pass the checkpointer
chatbot=graph.compile(checkpointer=checkpointer)


