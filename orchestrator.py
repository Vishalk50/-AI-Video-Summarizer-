#!/usr/bin/env python3
"""
orchestrator.py — Web Research Agent Pipeline

Fetches data from ANY source and extracts structured information for your agents.

Usage:
    python orchestrator.py run --url "https://..."      # Any webpage or YouTube
    python orchestrator.py run --search "query"          # Web search + fetch top result
    python orchestrator.py run --youtube "YT_URL"        # YouTube specific (with summary)
    python orchestrator.py status                        # Pipeline state
    python orchestrator.py stats                         # Stats
"""
import argparse
import io
import json
import sys
from datetime import datetime
from pathlib import Path

# Force UTF-8 for Unicode output (Hindi, etc.)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent))

from agents.extractor.extractor import WebExtractor
from context import update_state, read_context


def cmd_run_url(url: str, provider: str = "gemini"):
    """Fetch and extract data from any URL (webpage or YouTube)."""
    print(f"\n{'='*50}")
    print(f"WEB RESEARCH: {url}")
    print(f"{'='*50}\n")

    update_state({"pipeline": "fetching", "status": "running"})

    # Step 1: Extract
    print("1. Extractor — fetching content...")
    result = WebExtractor.extract(url)

    if result.get("error"):
        print(f"   Error: {result['error']}")
        return

    title = result.get("title", "Untitled")
    content = result.get("content", "")
    source = result.get("source", "unknown")
    print(f"   Source: {source}")
    print(f"   Title: {title}")
    print(f"   Content: {len(content)} chars")

    if not content:
        print("   No content extracted.")
        return

    # Step 2: If YouTube and we have a summary pipeline, run it
    summary_output = ""
    if source == "youtube" and provider:
        update_state({"pipeline": "summarizing", "status": "running"})
        print(f"\n2. Summarizer — generating summary via {provider}...")
        try:
            from agents.summarizer.summarizer import Summarizer
            s = Summarizer()
            transcript = result.get("transcript", "")
            transcript_time = result.get("transcript_time", "")

            summary = s.summarize(transcript, "summary", provider)
            print(f"   Summary: {len(summary)} chars")

            chapters = s.summarize(transcript_time, "timestamp", provider)
            print(f"   Chapters: {len(chapters)} chars")

            from agents.formatter.formatter import build_markdown, format_timestamps
            summary_output = build_markdown(title, summary, chapters, url)
            summary_output = format_timestamps(summary_output, url)
        except Exception as e:
            print(f"   Summary skipped: {e}")

    # Step 3: Save output
    update_state({"pipeline": "saving", "status": "running"})
    safe_title = "".join(c for c in title if c.isalnum() or c in " _-").strip()[:50] or "untitled"
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save raw content
    raw_path = output_dir / f"{safe_title}_raw.md"
    raw_content = f"# {title}\n\nSource: {url}\nFetched: {datetime.now().isoformat()}\n\n---\n\n{content}"
    raw_path.write_text(raw_content, encoding="utf-8")
    print(f"\n   Raw content: {raw_path}")

    # Save structured output to context.md
    from context import CONTEXT_FILE
    ctx_entry = f"""
## Web Research Result

- **URL:** {url}
- **Title:** {title}
- **Source:** {source}
- **Content Length:** {len(content)} chars
- **Fetched At:** {datetime.now().isoformat()}

### Raw Content Preview
{content[:2000]}

### Full Content
{content}
"""
    if summary_output:
        ctx_entry += f"\n### AI Summary\n{summary_output}\n"

    # Update context.md
    ctx_text = CONTEXT_FILE.read_text(encoding="utf-8")
    ctx_text = re.sub(r"## Agent Output\n.*?(?=\n##|\Z)", "", ctx_text, flags=re.DOTALL)
    ctx_text += f"\n## Agent Output\n{ctx_entry}\n"
    CONTEXT_FILE.write_text(ctx_text, encoding="utf-8")

    update_state({"pipeline": "complete", "status": "idle"})

    print(f"\n{'='*50}")
    print("DONE — Data is in context.md")
    print(f"{'='*50}")
    print(f"\nTitle: {title}")
    print(f"Content: {len(content)} chars")
    if summary_output:
        # Show first 500 chars of summary
        print(f"\n{summary_output[:500]}...")


def cmd_run_youtube(url: str, provider: str = "gemini"):
    """YouTube-specific pipeline with full summary."""
    cmd_run_url(url, provider)


def cmd_run_search(query: str, provider: str = "gemini"):
    """Search web, extract top result."""
    print(f"\n{'='*50}")
    print(f"WEB SEARCH: {query}")
    print(f"{'='*50}\n")

    update_state({"pipeline": "searching", "status": "running"})

    print("1. Searching...")
    results = WebExtractor.search(query)

    if results.get("error"):
        print(f"   Search error: {results['error']}")
        return

    print(f"   Found {results['result_count']} results")

    for i, r in enumerate(results.get("results", []), 1):
        print(f"   {i}. {r['title']}")
        print(f"      {r['url']}")
        print(f"      {r['snippet'][:100]}")

    # Fetch the top result automatically
    if results["results"]:
        top = results["results"][0]
        print(f"\n2. Fetching top result: {top['title']}")
        cmd_run_url(top["url"], provider)
    else:
        print("\nNo results found.")


def cmd_status():
    ctx = read_context()
    print(f"\nPipeline: {ctx.get('pipeline', 'idle')}")
    print(f"Status:   {ctx.get('status', 'waiting')}")

    # Show latest research result
    try:
        from context import CONTEXT_FILE
        text = CONTEXT_FILE.read_text(encoding="utf-8")
        if "## Agent Output" in text:
            section = text.split("## Agent Output")[1].split("##")[0].strip()
            print(f"\nLast Research:\n{section[:500]}")
    except Exception:
        pass


def cmd_stats():
    ctx = read_context()
    output_dir = Path("data")
    files = list(output_dir.glob("*_raw.md")) if output_dir.exists() else []
    print(f"\nStats:")
    print(f"  Research runs: {len(files)}")
    print(f"  Pipeline: {ctx.get('pipeline', 'idle')}")


import re  # noqa: needed for context.md manipulation


def main():
    parser = argparse.ArgumentParser(description="Web Research Agent")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status", help="Show pipeline state")

    url_p = sub.add_parser("run", help="Fetch data from any URL")
    url_p.add_argument("--url", help="Any URL (webpage or YouTube)")
    url_p.add_argument("--search", help="Web search query")
    url_p.add_argument("--youtube", help="YouTube URL")
    url_p.add_argument("--provider", default="gemini", choices=["gemini", "openai"])

    sub.add_parser("stats", help="Show stats")

    args = parser.parse_args()

    if args.command == "run":
        if args.youtube:
            cmd_run_youtube(args.youtube, args.provider)
        elif args.search:
            cmd_run_search(args.search, args.provider)
        elif args.url:
            cmd_run_url(args.url, args.provider)
        else:
            print("Provide --url, --search, or --youtube")
    elif args.command == "status":
        cmd_status()
    elif args.command == "stats":
        cmd_stats()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
