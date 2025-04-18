import requests
import tempfile
import os
import torch
import whisper
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL

def extract_plain_text(post_json: dict) -> str:
    """
    Extracts and returns plain text from a post JSON containing HTML content.
    """
    content_html = post_json.get("content", "")
    soup = BeautifulSoup(content_html, "html.parser")
    return soup.get_text(separator=" ", strip=True)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base", device=device)

def transcribe_youtube_link(post_json: dict) -> str:
    """
    Downloads audio from a YouTube link in the post's card or content, then transcribes it via local Whisper.
    """
    # Extract video URL from card or content
    card = post_json.get("card", {})
    video_url = card.get("url")
    if not video_url:
        soup = BeautifulSoup(post_json.get("content", ""), "html.parser")
        a = soup.find("a")
        video_url = a["href"] if a and a.get("href") else None
    if not video_url or "youtu" not in video_url:
        raise ValueError("No YouTube URL found in post JSON.")

    # Download audio via yt_dlp
    temp_dir = tempfile.gettempdir()
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': os.path.join(temp_dir, '%(id)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        audio_path = ydl.prepare_filename(info)

    # Transcribe with Whisper locally
    result = model.transcribe(audio_path)
    return result.get("text", "")

def transcribe_media_content(post_json: dict) -> str:
    """
    Downloads a video attachment from the post and transcribes its audio via local Whisper.
    """
    media = post_json.get("media_attachments", [])
    if not media:
        return ""

    # Find first video attachment
    media_url = None
    for m in media:
        if m.get("type") == "video" and m.get("url"):
            media_url = m["url"]
            break
    if not media_url:
        raise ValueError("No video media found in post JSON.")

    # Download media
    resp = requests.get(media_url, stream=True)
    resp.raise_for_status()
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        for chunk in resp.iter_content(chunk_size=8192):
            tmp.write(chunk)
        tmp_path = tmp.name

    # Transcribe with Whisper locally
    result = model.transcribe(tmp_path)
    return result.get("text", "")

def get_post_content(post_json: dict) -> str:
    """
    Routes a post JSON to the correct handler: transcribe_media_content for media,
    transcribe_youtube_link for YouTube links, or extract_plain_text for text.
    """
    # Prioritize video attachments
    if post_json.get("media_attachments"):
        return transcribe_media_content(post_json)

    # Next, check for embedded card with YouTube URL
    card = post_json.get("card", {}) or {}
    embed_url = card.get("url", "")
    if embed_url and "youtu" in embed_url:
        return transcribe_youtube_link(post_json)

    # Fallback: extract plain text
    return extract_plain_text(post_json)

# Alias for backward compatibility
get_content = get_post_content