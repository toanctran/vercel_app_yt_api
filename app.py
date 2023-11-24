from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi
import json
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
import requests

app = FastAPI()

@app.get("/")
async def root():
  return{"message":"hello world"}

@app.get("/api/get_transcript/{video_id}/{language}")
async def get_transcript(request: Request, video_id, language):
    transcript = YouTubeTranscriptApi.get_transcript(video_id, [f'{language}'])

    formatter = JSONFormatter()

    # .format_transcript(transcript) turns the transcript into a JSON string.
    json_formatted = formatter.format_transcript(transcript)
    return json_formatted

@app.get("/api/getYTVideoTitle/{video_id}")
async def get_yt_video_title(request: Request, video_id: str):
    try:
        # Replace 'YOUR_YOUTUBE_API_KEY' with your actual YouTube Data API key
        api_key = 'AIzaSyDV9XQkANrjxF9GF-30N6c0gm4GhuGZX3Y'

        # Make an HTTP GET request to the YouTube Data API
        response = requests.get(
            f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=snippet'
        )

        # Extract the video title from the API response
        video_title = response.json()['items'][0]['snippet']['title']

        return {"title": video_title}
    except Exception as e:
        return {"error": str(e)}