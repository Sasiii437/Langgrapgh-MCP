from youtube_transcript_api import YouTubeTranscriptApi
import re

def get_youtube_transcript(url: str) -> dict:
    """Fetches transcript from a given YouTube URL."""
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if not video_id_match:
        return {"error": "Invalid YouTube URL"}

    video_id = video_id_match.group(1)
    pr=YouTubeTranscriptApi()
    try:
        transcript = pr.fetch(video_id)
        transcript_text = " ".join([snippet.text for snippet in transcript.snippets])
        return {"transcript": transcript_text}
    except Exception as e:
        return {"error": str(e)}

# Example usage
print(get_youtube_transcript("https://www.youtube.com/watch?v=3OafqAbi_nQ"))
