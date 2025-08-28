from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.agents import initialize_agent,tool
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
#from langchain_mcp_adapters.client import 
import os


load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=os.getenv("GOOGLE_API"))

# response=llm.invoke("WHo are you")
# print(response.content)

basic_prompt=ChatPromptTemplate.from_messages(
    [
        (

            "System","You were a great problem solver and tech supporter and a well knowledged humanity while giving the answers "
        ),
        MessagesPlaceholder(variable_name="messages")
    ]
)

llm_chain=basic_prompt|llm

