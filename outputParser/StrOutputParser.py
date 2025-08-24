from langchain_core.output_parsers import PydanticOutputParser,StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate,HumanMessagePromptTemplate,SystemMessagePromptTemplate
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from os import getenv

load_dotenv()

llm = ChatOpenAI(
  api_key=getenv("OPENROUTER_API_KEY"),
  base_url=getenv("OPENROUTER_BASE_URL"),
  
  model=getenv("OPENROUTER_MODEL"),  # Replace with your desired model
  temperature=0.7,
 
)
parser=StrOutputParser()
prompt=PromptTemplate(
    template="{question}",
    input_variables=['question'])

# String Output Parser and the difference between normal response.content and StrOutputParser is that stroutputparser removes the leading and trailing double quotes and supports the chain formattion.

# Note stroutputparser doesn't support the get_formated_instruction so we use directly on the output of the model 


response = parser.invoke(llm.invoke(prompt.invoke({"question":"write a function that returns the sum of two numbers"})))
print("String Output Parser: ", response)
print("String Output Parser Type: ", type(response))