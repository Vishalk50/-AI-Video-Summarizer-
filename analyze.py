import sys
import os
from dotenv import load_dotenv
from src.video_info import GetVideo
from src.model import Model
from src.prompt import Prompt

load_dotenv()

if len(sys.argv) < 2:
    print("Usage: python analyze.py <youtube-url>")
    sys.exit(1)

url = sys.argv[1]

import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("-- Fetching video info...")
title = GetVideo.title(url)
print(f"-- Video: {title}")

print("-- Fetching transcript...")
transcript = GetVideo.transcript(url)
if not transcript or transcript.startswith("⚠️"):
    print(f"Error: {transcript}")
    sys.exit(1)

print(f"-- Transcript length: {len(transcript)} chars")

# Save transcript to file for analysis
os.makedirs("transcripts", exist_ok=True)
safe_title = "".join(c for c in title if c.isalnum() or c in " _-").strip()[:50]
with open(f"transcripts/{safe_title}.txt", "w", encoding="utf-8") as f:
    f.write(transcript)

print(f"-- Transcript saved to transcripts/{safe_title}.txt")
print(f"\n{'='*60}")
print(transcript[:5000])
if len(transcript) > 5000:
    print(f"\n... [{len(transcript) - 5000} more chars] ...")
