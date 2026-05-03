"""
formatter.py — Format summaries with timestamps and structure.
"""
import re


def format_timestamps(text: str, video_url: str, video_id: str | None = None) -> str:
    """Convert (time:HH:MM:SS) markers into clickable YouTube timestamp links."""
    def _replace(match):
        ts = match.group(1)
        parts = ts.split(":")
        total_secs = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        url = video_url.split("&")[0]
        return f"[{ts}]({url}?t={total_secs})"

    return re.sub(r"\(time:(\d{2}:\d{2}:\d{2})\)", _replace, text)


def build_markdown(title: str, summary: str, chapters: str = "",
                   video_url: str = "") -> str:
    """Build the final markdown output."""
    parts = [f"# {title}\n"]

    if video_url:
        parts.append(f"[ Watch on YouTube ]({video_url})\n")

    if chapters:
        parts.append("## Chapters\n")
        formatted = format_timestamps(chapters, video_url)
        parts.append(formatted + "\n")

    parts.append("## Summary\n")
    parts.append(summary + "\n")

    return "\n".join(parts)
