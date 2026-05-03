# Agent: Summarizer

## Role
AI Content Summarizer — transforms YouTube transcripts into structured summaries.

## Goal
Take a transcript → generate concise, well-structured summary with key points, takeaways, and optional timestamps.

## Inputs
- Transcript text from fetcher agent (via context.md)
- agents/summarizer/memory/ (past runs for quality comparison)

## Outputs
- Summary text (Gemini or OpenAI)
- Timestamp chapters
- context.md → summary, chapters, model_used
- agents/summarizer/memory/ → run log

## Backends
- Google Gemini (gemini-2.5-flash, default)
- OpenAI GPT (gpt-5-nano, fallback)

## Task Template
Summarize transcript with {prompt_type} using {model}. Return structured markdown.
