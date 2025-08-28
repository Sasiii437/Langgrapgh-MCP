from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os
import asyncio
import nest_asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import streamlit as st

# Patch event loop for Streamlit compatibility
nest_asyncio.apply()

# Load environment variables
load_dotenv()
#RENDER_URL = os.getenv("RENDER_URL")

# Initialize LLM and MCP client
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.getenv("GOOGLE_API"))
client = MultiServerMCPClient({
    "server": {
        "url": "https://langgrapgh-mcp.onrender.com/mcp",
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
st.title("LangGraph Agent with MCP server")
st.markdown(
    "Interact with a Gemini-powered LangGraph agent that dynamically uses tools exposed via our MCP server. "
    "Enter a prompt below and let the agent decide how to respond using available tools like:\n"
    "- 📺 YouTube Summariser (paste video link)\n"
    "- 🌐 Web Search\n"
    "- 🕒 Current Date & Time"
)

# Multiline input box
user_input = st.text_area("💬 Enter your prompt", height=150, placeholder="e.g. Summarize this YouTube video: https://www.youtube.com/watch?v=abc123")

# Submit button
submit = st.button("🚀 Send")

# Response area
if submit and user_input.strip():
    with st.spinner("Thinking..."):
        response = asyncio.create_task(run_agent(user_input))
        response = asyncio.get_event_loop().run_until_complete(response)
        st.markdown("### 🧠 Agent Response")
        st.success(response)
