 # AI-Video-Summarizer

  An AI-powered tool that fetches YouTube transcripts and generates smart summaries using Gemini API.

  Built with multi-agent architecture:
  - **Extractor agent** — fetches YouTube transcripts or web content
  - **Summarizer agent** — generates AI summaries via Gemini/OpenAI
  - **Formatter agent** — formats output with timestamps and markdown

  ## Features

  - YouTube video summarization (AI-powered)
  - Timestamp generation with chapter markers
  - Transcript extraction
  - Public shareable summary pages (FastAPI + OG tags)
  - Web search and content extraction
  - Supports Gemini and OpenAI models

  ## Tech Stack

  Python · Streamlit · FastAPI · Gemini API · OpenAI API · YouTube Transcript API

  ## Quick Start

  ```bash
  pip install -r requirements.txt
  streamlit run app.py
  ```