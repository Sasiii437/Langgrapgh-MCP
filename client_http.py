from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

client = MultiServerMCPClient({
    "server": {
        "url": "http://localhost:8000/mcp",
        "transport": "streamable_http",
    }
})

async def main():
    tools = await client.get_tools()
    print([tool.name for tool in tools])

asyncio.run(main())
