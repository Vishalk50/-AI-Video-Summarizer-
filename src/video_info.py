from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
import requests
import re

class GetVideo:
    @staticmethod
    def Id(link):
        """Extracts the video ID from a YouTube video link."""

        pattern = r"(?:v=|youtu\.be/)([0-9A-Za-z_-]{11})"

        match = re.search(pattern, link)

        if match:
            return match.group(1)

        return None

    @staticmethod
    def title(link):
        """Gets the title of a YouTube video."""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            r = requests.get(link, headers=headers, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")

            title = soup.find("meta", itemprop="name")["content"]
            return title

        except Exception:
            return "⚠️ Unable to fetch video title. Check the YouTube link."

    @staticmethod
    def channel(link):
        """Gets the channel/author name of a YouTube video."""
        try:
            r = requests.get(
                f"https://www.youtube.com/oembed?url={link}&format=json",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10
            )
            data = r.json()
            return data.get("author_name", "")
        except Exception:
            return ""

    @staticmethod
    def thumbnail(link):
        """Gets the thumbnail URL for a YouTube video."""
        video_id = GetVideo.Id(link)
        if video_id:
            return f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
        return ""

    @staticmethod
    def _get_transcript(video_id):
        """Fetch transcript with language fallback. Returns (transcript_list, language)."""
        api = YouTubeTranscriptApi()
        tl = api.list(video_id)

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

        available = [t.language_code for t in tl]
        if available:
            t = tl.find_transcript([available[0]])
            return t, available[0]

        raise Exception("No transcript available")

    @staticmethod
    def transcript(link):
        """Gets the transcript of a YouTube video."""
        video_id = GetVideo.Id(link)
        if not video_id:
            return "⚠️ Invalid YouTube link."
        try:
            t, lang = GetVideo._get_transcript(video_id)
            data = t.fetch()
            return " ".join(snippet.text for snippet in data)
        except Exception as e:
            return f"⚠️ Transcript error: {e}"

    @staticmethod
    def transcript_time(link):
        """Gets transcript with timestamps."""
        video_id = GetVideo.Id(link)
        if not video_id:
            return "⚠️ Invalid YouTube link."
        try:
            t, lang = GetVideo._get_transcript(video_id)
            data = t.fetch()
            parts = []
            for snippet in data:
                secs = int(snippet.start)
                h, m, s = secs // 3600, (secs % 3600) // 60, secs % 60
                parts.append(f"{snippet.text} (time:{h:02d}:{m:02d}:{s:02d})")
            return " ".join(parts)
        except Exception as e:
            return f"⚠️ Transcript error: {e}"
