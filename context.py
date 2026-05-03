"""
context.py — Shared Blackboard Manager for AI-Video-Summarizer.
"""
import re
from datetime import datetime
from pathlib import Path
from typing import Any

CONTEXT_FILE = Path(__file__).parent / "context.md"


def read_context() -> dict:
    if not CONTEXT_FILE.exists():
        return {"pipeline": "idle", "status": "waiting"}
    text = CONTEXT_FILE.read_text(encoding="utf-8")
    state = {}
    match = re.search(r"## Current State\n\n(.+?)(?:\n\n##|\Z)", text, re.DOTALL)
    if match:
        for line in match.group(1).split("\n"):
            line = line.strip().strip("- ")
            if ":**" in line:
                key, val = line.split(":**", 1)
                state[key.strip().lower()] = val.strip()
    return state


def update_state(updates: dict):
    if not CONTEXT_FILE.exists():
        CONTEXT_FILE.write_text("# Project Context\n\n## Current State\n", encoding="utf-8")
    text = CONTEXT_FILE.read_text(encoding="utf-8")
    lines = []
    for key, value in updates.items():
        label = key.replace("_", " ").title()
        lines.append(f"- **{label}:** {value}")
    new_state = "\n".join(lines)
    pattern = r"(## Current State\n\n).+?(\n\n##|\Z)"
    if re.search(pattern, text, re.DOTALL):
        text = re.sub(pattern, rf"\1{new_state}\2", text, count=1, flags=re.DOTALL)
    else:
        text = text.replace("---\n\n", f"---\n\n## Current State\n\n{new_state}\n\n", 1)
    CONTEXT_FILE.write_text(text, encoding="utf-8")
