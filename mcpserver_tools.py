from mcp.server.fastmcp import FastMCP
import datetime
# from langchain_community.tools import TavilySearchResults
from dotenv import load_dotenv
import os
import httpx
import re
from youtube_transcript_api import YouTubeTranscriptApi



load_dotenv()
port= int(os.environ.get("PORT", 8000))
mcp=FastMCP("Useful",host="0.0.0.0",port=port)

@mcp.tool()
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """ Returns the current date and time of the system in the specified format """

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time

# tavily_tool = TavilySearchResults(max_results=5)
# Tavily API details
TAVILY_API_KEY = os.getenv("TAVILY_API")
TAVILY_SEARCH_URL = "https://api.tavily.com/search"

async def search_tavily(query: str) -> dict:
    """Performs a Tavily web search and returns 5 results."""
    if not TAVILY_API_KEY:
        return {"error": "Tavily API key is missing. Set it in your .env file."}

    payload = {
        "query": query,
        "topic": "general",
        "search_depth": "basic",
        "chunks_per_source": 3,
        "max_results": 5,  # Fixed 
        "time_range": None,
        "days": 3,
        "include_answer": True,
        "include_raw_content": False,
        "include_images": False,
        "include_image_descriptions": False,
        "include_domains": [],
        "exclude_domains": []
    }

    headers = {
        "Authorization": f"Bearer {TAVILY_API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(TAVILY_SEARCH_URL, json=payload, headers=headers, timeout=30.0)
        response.raise_for_status()
        return response.json()
    

@mcp.tool()
async def search_agent(query:str):
    """ Returns the web search results , you can get to know most recent or current updates through the web search results """
    results = await search_tavily(query)

    if isinstance(results, dict):
        return {"results": results.get("results", [])}  # Ensure always returning a dictionary
    else:
        return {"error": "Unexpected Tavily response format"}
    
@mcp.tool()
def get_youtube_transcript(url: str):
    """Fetches transcript from a given YouTube URL."""
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    #video_id=url[-1:-12:1]
    if not video_id_match:
    #if not video_id:
        return {"error": "Invalid YouTube URL"}

    video_id = video_id_match.group(1)

    yout=YouTubeTranscriptApi()
    try:
        transcript =yout.fetch(video_id)
        transcript_text = " ".join([snippet.text for snippet in transcript.snippets])
        return {"transcript": transcript_text}
    except Exception as e:
        return {"error": str(e)}




#The transport="stdio" argument tells the server to:

#Use standard input/output (stdin and stdout) to receive and respond to tool function calls.

if __name__=="__main__":
    mcp.run(transport="streamable-http",mount_path="/mcp")