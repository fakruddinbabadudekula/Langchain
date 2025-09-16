import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
# 2. Initialize Gemini 2.5 Pro
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0.7,
)

# 3. Invoke with a simple prompt
response = llm.invoke("Explain quantum computing in simple terms.")
print(response.content)
