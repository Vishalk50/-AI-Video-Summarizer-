"""
publish.py — Save summaries as public shareable pages.

Both the Streamlit app and the FastAPI server use this.
Every summary generated gets saved to public/{video_id}/data.json
so the server can serve it as a beautiful shareable page.
"""
import json
from pathlib import Path
from datetime import datetime

PUBLIC_DIR = Path(__file__).parent / "public"


def save_summary(
    video_id: str,
    video_title: str,
    summary: str,
    channel: str = "",
    thumbnail: str = "",
) -> dict:
    """Save a summary as a public shareable page. Returns the data dict."""
    data = {
        "video_id": video_id,
        "video_title": video_title,
        "summary": summary,
        "channel": channel,
        "thumbnail": thumbnail,
        "created_at": datetime.now().isoformat(),
    }
    out_dir = PUBLIC_DIR / video_id
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "data.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data


def get_all_summaries() -> list[dict]:
    """Return all published summaries, newest first."""
    summaries = []
    if not PUBLIC_DIR.exists():
        return summaries
    for d in PUBLIC_DIR.iterdir():
        if not d.is_dir():
            continue
        data_file = d / "data.json"
        if data_file.exists():
            try:
                data = json.loads(data_file.read_text(encoding="utf-8"))
                summaries.append(data)
            except (json.JSONDecodeError, KeyError):
                continue
    summaries.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return summaries
