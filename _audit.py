"""Quick audit: show current state + test features."""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from agents.extractor.extractor import WebExtractor

print("=" * 50)
print("AUDIT: Web Research Agent")
print("=" * 50)

# 1. Search test
print("\n[1] Search Test: 'mandi price India 2026'")
try:
    r = WebExtractor.search("mandi price India 2026", 3)
    print(f"  Status: {'OK' if r['result_count'] > 0 else 'FAILED'}")
    print(f"  Results: {r['result_count']}")
    for res in r['results']:
        print(f"    - {res['title'][:70]}")
except Exception as e:
    print(f"  ERROR: {e}")

# 2. Webpage fetch test
print("\n[2] Webpage Test: https://example.com")
try:
    r2 = WebExtractor.extract_webpage("https://example.com")
    ok = r2['content_length'] > 0 and 'Example' in r2['title']
    print(f"  Status: {'OK' if ok else 'FAILED'}")
    print(f"  Title: {r2['title']}")
    print(f"  Content: {r2['content_length']} chars")
except Exception as e:
    print(f"  ERROR: {e}")

# 3. YouTube test
print("\n[3] YouTube Test: dQw4w9WgXcQ")
try:
    r3 = WebExtractor.extract_youtube("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    ok = len(r3['transcript']) > 100
    print(f"  Status: {'OK' if ok else 'FAILED'}")
    print(f"  Title: {r3['title']}")
    print(f"  Transcript: {len(r3['transcript'])} chars")
except Exception as e:
    print(f"  ERROR: {e}")

# 4. Check context.md pollution
print("\n[4] Context.md Health")
from pathlib import Path
ctx = Path("context.md").read_text(encoding="utf-8")
agent_outputs = ctx.count("## Agent Output")
print(f"  Agent Output sections: {agent_outputs}")
print(f"  File size: {len(ctx)} chars")
if agent_outputs > 1 or len(ctx) > 5000:
    print(f"  ISSUE: context.md growing unbounded!")

# 5. Check data/ folder
print("\n[5] Data Folder")
data_files = list(Path("data").glob("*")) if Path("data").exists() else []
print(f"  Files: {len(data_files)}")
for f in data_files:
    print(f"    {f.name} ({f.stat().st_size} bytes)")

# 6. Check garbled content
print("\n[6] Garbled Content Check")
for f in data_files:
    text = f.read_text(encoding="utf-8", errors="replace")
    garbled = sum(1 for c in text if ord(c) > 127 and ord(c) < 256)
    if garbled > len(text) * 0.3:
        print(f"  ISSUE: {f.name} - {garbled}/{len(text)} chars are garbled")

print("\n" + "=" * 50)
print("AUDIT COMPLETE")
print("=" * 50)
