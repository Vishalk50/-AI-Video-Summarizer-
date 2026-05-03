# Agent: Formatter

## Role
Output Formatter — structures AI summaries with proper timestamps, links, and markdown.

## Goal
Take raw summary + timestamp data → produce clean, clickable, well-formatted markdown output.

## Inputs
- Summary text from summarizer agent (via context.md)
- Timestamp chapters
- YouTube URL

## Outputs
- Formatted markdown with clickable timestamp links
- context.md → formatted_output
- agents/formatter/memory/ → format log

## Task Template
Format summary with timestamps for YouTube video: {url}
