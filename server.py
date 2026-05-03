"""
server.py — Public shareable summary pages (FastAPI)

Serves beautifully rendered summary pages with OG tags for social sharing.
This is the viral growth engine: every summary becomes a shareable landing page.

Run:
    uvicorn server:app --reload --port 8000
"""
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from publish import get_all_summaries, save_summary, PUBLIC_DIR

app = FastAPI(title="AI Video Summarizer")

# Ensure public dir exists
PUBLIC_DIR.mkdir(exist_ok=True)


def load_summary(video_id: str) -> dict | None:
    data_file = PUBLIC_DIR / video_id / "data.json"
    if not data_file.exists():
        return None
    return eval(data_file.read_text(encoding="utf-8"))


SHARE_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — AI Summary</title>
    <meta name="description" content="AI-powered summary of {video_title}. Get key takeaways, timestamps, and insights in minutes.">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:title" content="{video_title} — AI Summary">
    <meta property="og:description" content="AI-powered summary with key takeaways and insights.">
    <meta property="og:image" content="{thumbnail}">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{video_title} — AI Summary">
    <meta name="twitter:description" content="AI-powered summary with key takeaways and insights.">
    <meta name="twitter:image" content="{thumbnail}">

    <style>
        :root {{
            --bg: #0a0a0f;
            --surface: #12121a;
            --border: #1e1e2e;
            --text: #e4e4ef;
            --text-dim: #8888a0;
            --accent: #6c5ce7;
            --accent-hover: #7d6ff0;
            --radius: 12px;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.7;
            -webkit-font-smoothing: antialiased;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        .header {{
            text-align: center;
            padding: 40px 0;
            border-bottom: 1px solid var(--border);
            margin-bottom: 40px;
        }}
        .header h1 {{
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--accent);
            margin-bottom: 8px;
        }}
        .header p {{
            color: var(--text-dim);
            font-size: 14px;
        }}
        .video-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            overflow: hidden;
            margin-bottom: 32px;
        }}
        .video-card img {{
            width: 100%;
            display: block;
        }}
        .video-card-body {{
            padding: 24px;
        }}
        .video-card-body h2 {{
            font-size: 20px;
            margin-bottom: 12px;
            line-height: 1.4;
        }}
        .video-card-body .meta {{
            color: var(--text-dim);
            font-size: 14px;
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
        }}
        .summary-content {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 32px;
            margin-bottom: 32px;
        }}
        .summary-content h3 {{
            font-size: 18px;
            margin-bottom: 16px;
            color: var(--accent);
        }}
        .summary-content p {{
            margin-bottom: 16px;
            color: var(--text);
        }}
        .summary-content ul {{
            margin: 0 0 16px 20px;
            color: var(--text);
        }}
        .summary-content li {{
            margin-bottom: 8px;
        }}
        .share-bar {{
            display: flex;
            gap: 12px;
            margin-bottom: 32px;
            flex-wrap: wrap;
        }}
        .share-btn {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 20px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: var(--surface);
            color: var(--text);
            font-size: 14px;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.2s;
        }}
        .share-btn:hover {{
            border-color: var(--accent);
            background: rgba(108,92,231,0.1);
        }}
        .cta {{
            background: linear-gradient(135deg, var(--accent), #a855f7);
            border-radius: var(--radius);
            padding: 48px 32px;
            text-align: center;
        }}
        .cta h3 {{
            font-size: 24px;
            margin-bottom: 8px;
        }}
        .cta p {{
            color: rgba(255,255,255,0.8);
            margin-bottom: 24px;
            font-size: 15px;
        }}
        .cta-btn {{
            display: inline-block;
            padding: 14px 36px;
            background: white;
            color: var(--accent);
            font-weight: 600;
            border-radius: 8px;
            text-decoration: none;
            font-size: 16px;
            transition: transform 0.2s;
        }}
        .cta-btn:hover {{
            transform: translateY(-2px);
        }}
        .footer {{
            text-align: center;
            padding: 40px 0;
            color: var(--text-dim);
            font-size: 13px;
        }}
        .footer a {{
            color: var(--accent);
            text-decoration: none;
        }}
        .recent-list {{
            display: grid;
            gap: 12px;
            margin: 24px 0;
        }}
        .recent-item {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 16px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            text-decoration: none;
            color: var(--text);
            transition: border-color 0.2s;
        }}
        .recent-item:hover {{
            border-color: var(--accent);
        }}
        .recent-item .title {{ font-weight: 500; }}
        .recent-item .date {{ color: var(--text-dim); font-size: 13px; }}
        .hero {{
            text-align: center;
            padding: 80px 0 40px;
        }}
        .hero h1 {{
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 12px;
        }}
        .hero p {{
            color: var(--text-dim);
            font-size: 18px;
            max-width: 500px;
            margin: 0 auto 32px;
        }}
        input[type="text"] {{
            width: 100%;
            max-width: 500px;
            padding: 14px 20px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: var(--surface);
            color: var(--text);
            font-size: 16px;
            outline: none;
        }}
        input[type="text"]:focus {{
            border-color: var(--accent);
        }}
        @media (max-width: 600px) {{
            .container {{ padding: 20px 16px; }}
            .hero h1 {{ font-size: 28px; }}
            .cta {{ padding: 32px 20px; }}
            .summary-content {{ padding: 20px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AI Video Summarizer</h1>
            <p>Turn any YouTube video into key takeaways</p>
        </div>

        {content}

        <div class="footer">
            <p>Built with AI &bull; <a href="/">Summarize your own video</a></p>
        </div>
    </div>
</body>
</html>"""


def render_summary_page(data: dict) -> str:
    """Render a summary page using the template."""
    video_title = data.get("video_title", "Untitled")
    summary = data.get("summary", "")
    video_id = data.get("video_id", "")
    thumbnail = data.get("thumbnail", "")
    channel = data.get("channel", "YouTube")
    created = data.get("created_at", "")

    # Format date
    try:
        dt = datetime.fromisoformat(created)
        date_str = dt.strftime("%B %d, %Y")
    except (ValueError, TypeError):
        date_str = ""

    canonical_url = f"/v/{video_id}"

    # Build content HTML
    summary_html = summary.replace("\n", "<br>") if summary else "<p>No summary available.</p>"

    content = f"""
    <div class="video-card">
        <img src="{thumbnail}" alt="{video_title}" loading="lazy">
        <div class="video-card-body">
            <h2>{video_title}</h2>
            <div class="meta">
                <span>📺 {channel}</span>
                {f'<span>📅 {date_str}</span>' if date_str else ''}
                <span>🎬 <a href="https://youtu.be/{video_id}" target="_blank" style="color:var(--accent);text-decoration:none;">Watch original</a></span>
            </div>
        </div>
    </div>

    <div class="summary-content">
        <h3>📄 AI Summary</h3>
        <div>{summary_html}</div>
    </div>

    <div class="share-bar">
        <a class="share-btn" href="https://twitter.com/intent/tweet?text={video_title} — AI Summary&url={canonical_url}" target="_blank">
            🐦 Share on Twitter
        </a>
        <a class="share-btn" href="https://www.linkedin.com/sharing/share-offsite/?url={canonical_url}" target="_blank">
            💼 Share on LinkedIn
        </a>
        <button class="share-btn" onclick="navigator.clipboard.writeText(window.location.href).then(()=>this.textContent='✅ Copied!').then(()=>setTimeout(()=>this.textContent='🔗 Copy Link',2000))">
            🔗 Copy Link
        </button>
    </div>

    <div class="cta">
        <h3>🎯 Summarize Any Video</h3>
        <p>Get AI-powered summaries, timestamps, and transcripts from any YouTube video.</p>
        <a class="cta-btn" href="/">Try It Now →</a>
    </div>
    """

    return SHARE_TEMPLATE.format(
        title=video_title,
        video_title=video_title,
        canonical_url=canonical_url,
        thumbnail=thumbnail,
        content=content
    )


@app.get("/", response_class=HTMLResponse)
async def landing_page():
    """Landing page with recent summaries and URL input."""
    summaries = get_all_summaries()[:12]

    recent_html = ""
    if summaries:
        items = ""
        for s in summaries:
            title = s.get("video_title", "Untitled")
            vid = s.get("video_id", "")
            created = s.get("created_at", "")[:10]
            items += f'<a class="recent-item" href="/v/{vid}"><span class="title">{title}</span><span class="date">{created}</span></a>'
        recent_html = f'<h3 style="margin-top:40px;margin-bottom:16px;">Recent Summaries</h3><div class="recent-list">{items}</div>'

    content = f"""
    <div class="hero">
        <h1>🎬 AI Video Summarizer</h1>
        <p>Paste a YouTube link and get an instant AI-powered summary with key takeaways.</p>
        <form action="/" method="get" onsubmit="event.preventDefault();window.location.href='/v/'+new URLSearchParams(new FormData(this)).get('url')">
            <input type="text" name="url" placeholder="https://youtube.com/watch?v=..." style="margin-bottom:12px;">
        </form>
        <p style="font-size:14px;margin-top:12px;">Or use the <a href="https://ai-video-summarizer.streamlit.app" style="color:var(--accent);">Streamlit app</a> to generate summaries.</p>
    </div>
    {recent_html}
    """

    return SHARE_TEMPLATE.format(
        title="AI Video Summarizer",
        video_title="Summarize YouTube Videos with AI",
        canonical_url="/",
        thumbnail="https://i.ytimg.com/vi/xDXVozOg-Kk/hqdefault.jpg",
        content=content
    )


@app.get("/v/{video_id}", response_class=HTMLResponse)
async def view_summary(video_id: str):
    """View a public summary page."""
    data = load_summary(video_id)
    if not data:
        raise HTTPException(status_code=404, detail="Summary not found")
    return render_summary_page(data)


@app.get("/recent")
async def recent_summaries():
    """JSON endpoint for recent summaries."""
    summaries = get_all_summaries()[:20]
    return JSONResponse(content=summaries)


@app.get("/api/health")
async def health():
    return {"status": "ok", "summaries": len(get_all_summaries())}


def publish_summary(
    video_id: str,
    video_title: str,
    summary: str,
    channel: str = "",
    thumbnail: str = "",
):
    """Called by the Streamlit app when a new summary is generated."""
    data = save_summary(video_id, video_title, summary, channel, thumbnail)
    # Also render and save static HTML for instant serving
    html = render_summary_page(data)
    (PUBLIC_DIR / video_id / "index.html").write_text(html, encoding="utf-8")
    return data


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
