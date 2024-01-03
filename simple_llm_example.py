from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

chat_model = ChatOpenAI(api_key=api_key)

result = chat_model.predict("Hello, how are you?")

print(result)