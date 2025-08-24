from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from os import getenv
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()


llm = ChatOpenAI(
  api_key=getenv("OPENROUTER_API_KEY"),
  base_url=getenv("OPENROUTER_BASE_URL"),
  model=getenv("OPENROUTER_MODEL") , # Replace with your desired model
  temperature=0.7,
 
)

prompt=PromptTemplate(
    template="Here is the user quesion{question} and give the output in this instruction formate{instructions}",input_variables=['question'],partial_variables={'instructions':JsonOutputParser().get_format_instructions()}
)
result=llm.invoke(prompt.invoke({'question':"Give me the prompt for an video generation model to instruct the to create the 3second video clip of ramayan with expressiong the details of each second."}))
print(result)
print(type(result.content))