# Agent: Extractor

## Role
Web Content Extractor — fetches and extracts structured data from ANY website.

## Goal
Take a URL or search query → fetch page content → extract relevant structured data → save to context.md for other agents.

## Inputs
- URL or search query from user (via orchestrator)
- agents/extractor/memory/ (learned extraction patterns)

## Outputs
- Structured markdown/data in context.md
- agents/extractor/memory/ → extraction log

## Capabilities
- YouTube transcript fetch (existing)
- Any webpage content extraction
- Web search (via Tavily or similar)
- AI-powered structured extraction

## Task Template
Fetch and extract data from: {url}
