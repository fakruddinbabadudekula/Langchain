import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

# 1. Set your API key (get it from Google AI Studio)
# os.environ["GOOGLE_API_KEY"] = "AIzaSyC6DUBPcvggno3qu_chqy0vGxjKDNUP24s"

# 2. Initialize Gemini 2.5 Pro
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    
    temperature=0.7,
)



prompt1=PromptTemplate(
    template="Can you detailed blog on the given topic from different perscpectives and here is the topic {topic}",
    input_variables=['topic']
)
prompt2=PromptTemplate(
    template="Can you give {lines} summery point from the given blog {blog}", 
    # This one trigger the error because if only one vairable the chain automatically pass to the variable but here two so missmatch solution is 
    # use lambda function between output and next prompt like this parser|lambda x:{blog:x,line:5}|prompt2
    input_variables=['blog','lines']
)

# chain=prompt1|llm|StrOutputParser()|prompt2|llm|StrOutputParser() 
# Recieved this error
# TypeError: Expected mapping type as input to PromptTemplate. Received <class 'str'>.
# For troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/INVALID_PROMPT_INPUT

chain=prompt1|llm|StrOutputParser()|(lambda x:{'blog':x,'lines':7})|prompt2|llm|StrOutputParser() 

# Here are 7 summery points from the blog "India's Economic Ascent: A Tapestry of Growth from Diverse Perspectives":

# 1.  **Sustained Macroeconomic Expansion:** India's economy has experienced consistent GDP growth, driven by its demographic dividend, a dominant services sector, manufacturing initiatives, rising consumption, and significant Foreign Direct Investment (FDI).
# 2.  **Business and Entrepreneurial Hub:** India offers vast opportunities for businesses and entrepreneurs due to its large domestic market and digital transformation, though challenges like regulatory hurdles and access to capital persist.
# 3.  **Progress in Human Development Amidst Inequality:** While economic growth has led to poverty reduction and improved living standards for many, significant challenges remain in addressing income inequality, unemployment, and ensuring quality education and healthcare for all. 
# 4.  **Growing Global Influence:** India's economic strength has amplified its role as a global economic player, enabling strategic partnerships and making it a significant source of talent and innovation worldwide.
# 5.  **Environmental Sustainability Challenges:** India's growth trajectory is intertwined with environmental concerns, including pollution and resource depletion, necessitating a focus on sustainable practices and renewable energy adoption.
# 6.  **Key Growth Drivers:** The blog highlights the demographic dividend, the services sector, manufacturing, rising consumption, and FDI as primary engines of India's economic expansion.
# 7.  **Balancing Act for Future Prosperity:** India's continued economic ascent requires a careful balance of various factors, including macroeconomic stability, fostering innovation, ensuring social equity, navigating global dynamics, and prioritizing environmental sustainability for inclusive and prosperous growth.

result=chain.invoke({
    'topic':"Indian Economic growth."
})
print(result)