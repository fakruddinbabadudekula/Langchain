from langchain_core.output_parsers import PydanticOutputParser
from pydantic import Field,BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from os import getenv
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0.7,
)
class Structure(BaseModel):
    name:str=Field(description="Name of the pompt i.e what should be the name of the prompt.")
    second_1:str=Field(description="Here is the script of the second_1 scence ")
    second_2:str=Field(description="Here is the script of the second_2 scence ")
    second_3:str=Field(description="Here is the script of the second_3 scence ")
    negative:str=Field(description="Here use the negative words whcih means to understand the model that thes things should not be to do like merging the pixels this one is negative thing and unordered seuquence that means there is a no reason to match the second_1 scipt with second_2 script and sooon ")
    instruction:str=Field(description="Here is the instructions that must be follow for the model")
    temperature:float=Field(lt=2,gt=-1,description="Here is the temperature value to manage the random ness in the model")

# parser=PydanticOutputParser(
#    pydantic_object= Structure
# )
# prompt=PromptTemplate(
#     template="Here is the user quesion{question} and give the output in this instruction formate{instructions}",input_variables=['question'],partial_variables={'instructions':parser.get_format_instructions()}
# )
# result=llm.invoke(prompt.invoke({'question':"Give me the prompt for an video generation model to instruct the to create the 3second video clip of ramayan with expressiong the details of each second."}))
# print(parser.parse(result.content))
# name='Ramayan 3-Second Visual Story' second_1="Open on Lord Rama standing serene amidst lush green forest. Sunlight filters through the leaves, creating dappled light on his face. He has a calm, contemplative expression, looking towards the horizon.  Focus on the peaceful atmosphere and Rama's inner strength.  Color palette: warm greens, golds, and soft blues." second_2='Quick transition to a scene depicting Ravana, imposing and menacing, with a cruel smile. He is shown holding a bow, aiming an arrow towards Rama.  His expression is filled with malice and aggression.  Color palette: deep reds, dark purples, and shadowy blacks.  Emphasis on dramatic lighting.' second_3="Close-up on Rama's face, displaying a determined and resolute expression. He raises his bow in response to Ravana's attack, his eyes focused and unwavering.  A hint of a smile plays on his lips, hinting at his inner power.  Color palette: vibrant oranges, bright yellows, and deep blues.  Dynamic composition." negative='pixel merging, blurry images, inconsistent character design, unnatural lighting, distorted expressions, chaotic scene, overlapping elements, low resolution, text overlays, static images' instruction="Create a 3-second video clip depicting a simplified visual story of the Ramayana. Each second should focus on a specific moment: Rama's serenity, Ravana's aggression, and Rama's determined response.  Maintain a consistent visual style throughout the clip, focusing on character expressions and dynamic composition.  The overall tone should be epic and dramatic, yet visually appealing. The video should be suitable for a children's audience and should be highly engaging.  Focus on conveying the essence of the story through visuals." temperature=0.7


# Note That the model doens't not strictly follow the rules for example if we set temperature as int but the most of the training data has the temperature in float so it may returns the temperature in float datatype so there is an error while parsing into pydantic so note it and make the datatypes of the value.

Structured_output_model=llm.with_structured_output(Structure)
structured_result=Structured_output_model.invoke("Give me the prompt for an video generation model to instruct the to create the 3second video clip of ramayan with expressiong the details of each second.")

print(structured_result)
# name='Ramayan' second_1='Create a scene of the Ramayana in which Ram is present in the jungle with Sita and Lakshman.' second_2='In the second scene, Sita is abducted by Ravan, and there is a fierce battle between Ram and Ravan.' second_3='In the third scene, Ram returns to Ayodhya with Sita and is crowned as the king.' negative='unordered sequence, merging pixels' instruction='Follow the instructions to generate a video of the Ramayana, ensuring that each scene is exactly one second long and the transitions are smooth.' temperature=0.7

# WHen we use the with structured output method the model returns directly structured output 
