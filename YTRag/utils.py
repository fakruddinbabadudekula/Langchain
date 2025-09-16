from youtube_transcript_api import YouTubeTranscriptApi,TranscriptsDisabled
from urllib.parse import urlparse, parse_qs




def yttranscript(video_id,lang='en'):
    """
    Fetching the transcript from the video ID"""

    try:
    # If you don’t care which language, this returns the “best” one
        transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=["en"])

    # Flatten it to plain text
        transcript = " ".join(chunk.text for chunk in transcript_list)
        return transcript

    except TranscriptsDisabled:
        print("No captions available for this video.")





def extract_video_id(url: str) -> str:
    """
    Extracts the YouTube video ID from a given URL.
    Supports both 'youtube.com' and 'youtu.be' formats.
    """
    parsed_url = urlparse(url)

    # Case 1: https://www.youtube.com/watch?v=VIDEO_ID
    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        query = parse_qs(parsed_url.query)
        return query.get("v", [None])[0]

    # Case 2: https://youtu.be/VIDEO_ID
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path.lstrip("/")

    return None


def yttranscript_from_url(url, lang="en"):
    """
    Fetching Transcripts from the url
    """
    video_id = extract_video_id(url)
    if not video_id:
        return "Invalid YouTube URL"
    return yttranscript(video_id, lang)