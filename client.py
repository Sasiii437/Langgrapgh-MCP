import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.getenv("GOOGLE_API"))

client = MultiServerMCPClient({
    "first_one": {
        "command": "C:/Users/chint/Downloads/LangGraph_MCP/mc_ag/Scripts/python.exe",
        "args": [r"C:\Users\chint\Downloads\LangGraph_MCP\mcpserver_tools.py"],
        "transport": "stdio",
    }
})

async def main():
    tools = await client.get_tools()
    print([tool.name for tool in tools])

asyncio.run(main())
