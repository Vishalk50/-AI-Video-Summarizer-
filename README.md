# Web Research Agent

Fetch data from ANY source and extract structured information for your AI agents.

## Usage

```bash
# Any webpage
python orchestrator.py run --url "https://example.com"

# YouTube video (with AI summary)
python orchestrator.py run --youtube "https://youtube.com/watch?v=..."

# Web search (auto-fetches top result)
python orchestrator.py run --search "latest AI trends 2026"
```

## Output
- **`context.md`** — Structured data ready for agent consumption
- **`data/`** folder — Raw content saved for reference
- **Console** — Real-time pipeline status

## Agents

| Agent | What It Does |
|-------|-------------|
| **extractor** | Fetch ANY URL (webpage, YouTube, search) + extract content |
| **summarizer** | AI summarization via Gemini or OpenAI |
| **formatter** | Markdown formatting |

## Examples

```bash
# Research a topic for your agents
python orchestrator.py run --search "vegetable mandi prices India 2026"

# Fetch a specific article
python orchestrator.py run --url "https://example.com/mandi-rates"

# Summarize a YouTube tutorial
python orchestrator.py run --youtube "https://youtube.com/watch?v=..."
```

## Streamlit UI

```bash
streamlit run app.py
```
