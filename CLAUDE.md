# AI-Video-Summarizer — Web Research Agent

## Mission
Fetch data from ANY source (webpage, YouTube, search) → extract structured information → feed to your personal agents via context.md.

## Architecture

```
User (URL / search query)
    │
    ▼
┌──────────────────────────────────────────────────────────┐
│                    PIPELINE                                │
│                                                           │
│  extractor → (optional: summarizer → formatter)           │
│       ↓                                                   │
│  context.md  ←─────── structured data for your agents     │
└──────────────────────────────────────────────────────────┘
```

## Agents

| Agent | Role | Code |
|-------|------|------|
| extractor | Fetch ANY URL (webpage/YouTube/search) + extract content | `agents/extractor/extractor.py` |
| summarizer | AI summarization (Gemini/OpenAI) | `agents/summarizer/summarizer.py` |
| formatter | Markdown formatting with timestamps | `agents/formatter/formatter.py` |
| fetcher | YouTube-specific transcript fetch | `agents/fetcher/fetcher.py` |

## Commands

```bash
# Any webpage
python orchestrator.py run --url "https://example.com"

# YouTube video (with AI summary)
python orchestrator.py run --youtube "YT_URL"

# Web search (fetches top result automatically)
python orchestrator.py run --search "your query"

# Check pipeline state
python orchestrator.py status
```

## Output Flow
1. Extractor fetches content from ANY source
2. Raw content saved to `data/` + context.md
3. If YouTube → summary + timestamps also generated
4. context.md holds structured data ready for other agents to consume
