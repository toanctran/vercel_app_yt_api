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
    

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Video Digest",
        version="1.0.0",
        summary="This is the Youtube transcript loader using FastAPI and Vercel",
        description="Use this to get the Youtube transcript for a Youtube video given Youtube video_id",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

with open('openapi.json', 'w') as f:
    json.dump(get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
    ), f)