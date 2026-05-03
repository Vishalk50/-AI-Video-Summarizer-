# Agent: Fetcher

## Role
YouTube Data Fetcher — extracts video ID, title, and transcript from YouTube URLs.

## Goal
Given a YouTube URL, return: video title, full transcript (plain), transcript with timestamps.

## Inputs
- YouTube URL from user (via context.md)

## Outputs
- context.md → video_id, title, transcript, transcript_time
- agents/fetcher/memory/ → fetch log

## Files
- `fetcher.py` — GetVideo class (ID, title, transcript, transcript_time)

## Task Template
Fetch transcript for YouTube URL: {url}
