"""
fetcher.py — Fetch YouTube transcript + video metadata.

Copy of src/video_info.py maintained here for agent structure.
Root src/video_info.py remains for backward compatibility.
"""
import re
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi


class GetVideo:
    @staticmethod
    def Id(link: str) -> str | None:
        pattern = r"(?:v=|youtu\.be/)([0-9A-Za-z_-]{11})"
        match = re.search(pattern, link)
        return match.group(1) if match else None

    @staticmethod
    def title(link: str) -> str:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(link, headers=headers, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            return soup.find("meta", itemprop="name")["content"]
        except Exception:
            return "Unable to fetch video title."

    @staticmethod
    def _get_transcript(video_id: str) -> tuple:
        """Fetch transcript with language fallback. Returns (transcript_list, language)."""
        api = YouTubeTranscriptApi()
        tl = api.list(video_id)

        # Try languages in order: en → hi → any available
        for lang in ['en', 'hi']:
            try:
                t = tl.find_transcript([lang])
                return t, lang
            except Exception:
                try:
                    t = tl.find_generated_transcript([lang])
                    return t, lang
                except Exception:
                    continue

        # Fallback: pick first available
        available = [t.language_code for t in tl]
        if available:
            t = tl.find_transcript([available[0]])
            return t, available[0]

        raise Exception("No transcript available")

    @staticmethod
    def transcript(link: str) -> str:
        video_id = GetVideo.Id(link)
        if not video_id:
            return "Invalid YouTube link."
        try:
            t, lang = GetVideo._get_transcript(video_id)
            data = t.fetch()
            return " ".join(snippet.text for snippet in data)
        except Exception as e:
            return f"Transcript error: {e}"

    @staticmethod
    def transcript_time(link: str) -> str:
        video_id = GetVideo.Id(link)
        if not video_id:
            return "Invalid YouTube link."
        try:
            t, lang = GetVideo._get_transcript(video_id)
            data = t.fetch()
            result = ""
            for snippet in data:
                result += snippet.text
                secs = int(snippet.start)
                h, m, s = secs // 3600, (secs % 3600) // 60, secs % 60
                result += f" (time:{h:02d}:{m:02d}:{s:02d}) "
            return result
        except Exception as e:
            return f"Transcript error: {e}"

    @staticmethod
    def fetch_all(link: str) -> dict:
        """Fetch everything: ID, title, transcript, timed transcript."""
        return {
            "video_id": GetVideo.Id(link),
            "title": GetVideo.title(link),
            "transcript": GetVideo.transcript(link),
            "transcript_time": GetVideo.transcript_time(link),
        }
