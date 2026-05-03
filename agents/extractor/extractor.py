"""
extractor.py — Web Content Fetcher & Extractor

Fetches content from ANY source:
  - YouTube videos (transcript + metadata)
  - Any webpage (text content)
  - Web search results
  - Raw URL content

Outputs structured data to context.md for consumption by other agents.
"""
import re
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


class WebExtractor:
    """Extract content from any web source."""

    @staticmethod
    def is_youtube_url(url: str) -> bool:
        return bool(re.search(r"(?:youtube\.com|youtu\.be)", url))

    @staticmethod
    def extract_youtube(url: str) -> dict:
        """YouTube transcript + title."""
        from agents.fetcher.fetcher import GetVideo
        video = GetVideo.fetch_all(url)
        return {
            "source": "youtube",
            "url": url,
            "title": video.get("title", ""),
            "transcript": video.get("transcript", ""),
            "transcript_time": video.get("transcript_time", ""),
            "content": video.get("transcript", ""),
        }

    @staticmethod
    def extract_webpage(url: str, max_chars: int = 50000) -> dict:
        """Extract readable text content from any webpage."""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/120.0.0.0 Safari/537.36"
            }
            resp = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(resp.text, "html.parser")

            # Remove script/style/nav elements
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            title = ""
            if soup.title:
                title = soup.title.get_text(strip=True)

            text = soup.get_text(separator="\n", strip=True)
            text = re.sub(r"\n{3,}", "\n\n", text)

            if len(text) > max_chars:
                text = text[:max_chars] + "\n\n[...truncated...]"

            return {
                "source": "webpage",
                "url": url,
                "title": title,
                "content": text,
                "content_length": len(text),
            }

        except Exception as e:
            return {
                "source": "webpage",
                "url": url,
                "title": "",
                "content": "",
                "error": str(e),
            }

    @staticmethod
    def extract(url: str) -> dict:
        """Auto-detect source type and extract accordingly."""
        if WebExtractor.is_youtube_url(url):
            return WebExtractor.extract_youtube(url)
        return WebExtractor.extract_webpage(url)

    @staticmethod
    def search(query: str, max_results: int = 5) -> dict:
        """Search the web using DuckDuckGo (free, no API key)."""
        results = []
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=max_results):
                    results.append({
                        "title": r.get("title", ""),
                        "url": r.get("href", ""),
                        "snippet": r.get("body", ""),
                    })

            return {
                "source": "search",
                "query": query,
                "results": results,
                "result_count": len(results),
            }
        except Exception as e:
            return {
                "source": "search",
                "query": query,
                "results": [],
                "error": str(e),
            }
