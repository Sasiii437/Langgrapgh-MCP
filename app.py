from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import streamlit as st

# Load environment variables
load_dotenv()
RENDER_URL=os.getenv("RENDER_URL")
# Initialize LLM and MCP client
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.getenv("GOOGLE_API"))
client = MultiServerMCPClient({
    "server": {
        "url": f"{RENDER_URL}/mcp",  
        "transport": "streamable_http",
    }
})

# System prompt for agent
system_message = SystemMessage(content=(
    "You have access to multiple tools that can help answer queries. "
    "Use them dynamically and efficiently based on the user's request."
))

# Async wrapper for agent invocation
async def run_agent(query):
    tools = await client.get_tools()
    agent = create_react_agent(llm, tools)
    agent_response = await agent.ainvoke({"messages": [system_message, HumanMessage(content=query)]})
    return agent_response["messages"][-1].content

# Streamlit UI
st.set_page_config(page_title="LangGraph MCP Agent", layout="centered")
st.title("🔧 LangGraph MCP Agent Interface")
st.markdown("Interact with a Gemini-powered LangGraph agent that dynamically uses tools exposed via our MCP server. Enter a prompt below and let the agent decide how to respond using available tools ( Youtube Summariser - video link, Web search , Current date & Time).")

# Input box and button
user_input = st.text_input("💬 Enter your prompt", placeholder="e.g. What's the weather in NYC?")
submit = st.button("🚀 Send")

# Response area
if submit and user_input:
    with st.spinner("Thinking..."):
        response = asyncio.run(run_agent(user_input))
        st.markdown("### 🧠 Agent Response")
        st.success(response)
