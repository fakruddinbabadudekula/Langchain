import os
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Set your API key (get it from Google AI Studio)
os.environ["GOOGLE_API_KEY"] = "AIzaSyC6DUBPcvggno3qu_chqy0vGxjKDNUP24s"

# 2. Initialize Gemini 2.5 Pro
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0.7,
)

# 3. Invoke with a simple prompt
response = llm.invoke("Explain quantum computing in simple terms.")
print(response.content)
