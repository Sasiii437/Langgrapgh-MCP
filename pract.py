from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import streamlit as st


load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=os.getenv("GOOGLE_API"))
client = MultiServerMCPClient({
    "server": {
        "url": "http://localhost:8000/mcp",
        "transport": "streamable_http",
    }
})



system_message = SystemMessage(content=(
                "You have access to multiple tools that can help answer queries. "
                "Use them dynamically and efficiently based on the user's request. "
        ))



async def run_agent():
    tools = await client.get_tools()
    agent = create_react_agent(
        llm,
        tools
    )

    query=input("Enter your prompt ")
    # a_response = await agent.ainvoke(
    #     {"messages": [{"role": "user", "content": {query}}]}
    # )
    agent_response = await agent.ainvoke({"messages": [system_message, HumanMessage(content=query)]})

    return agent_response["messages"][-1].content
# weather_response = await agent.ainvoke(
#     {"messages": [{"role": "user", "content": "what is the weather in nyc?"}]}
# )

if __name__ == "__main__":
    response = asyncio.run(run_agent())
    print("\nFinal Response:", response)
