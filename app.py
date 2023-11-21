from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi
import json
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter


app = FastAPI()

@app.get("/")
async def root():
  return{"message":"hello world"}

@app.get("/get_transcript/{video_id}")
async def get_transcript(request: Request, video_id):
  transcript = YouTubeTranscriptApi.get_transcript(video_id)

  formatter = JSONFormatter()

  # .format_transcript(transcript) turns the transcript into a JSON string.
  json_formatted = formatter.format_transcript(transcript)
  return json_formatted
    
