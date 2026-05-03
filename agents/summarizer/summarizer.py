"""
summarizer.py — AI Summarization via Gemini or OpenAI.
"""
import os
from dotenv import load_dotenv
from google import genai
from openai import OpenAI


PROMPTS = {
    "summary": """
You are an expert content summarizer. Transform the YouTube transcript below into a clear, structured summary.

## Output Format

### Video Overview
Brief intro and purpose of the video.

### Key Points
- Point 1 with explanation
- Point 2 with explanation
- Continue for all major topics.

### Key Takeaways
Most important lessons viewers should remember.

## Constraints
- Max 250 words
- Clear, simple language
- No filler or repetition
- Logical flow

## Transcript:
""",
    "timestamp": """
You are an AI that generates chapter timestamps for YouTube videos.

## Output Format (strict)
1. [hh:mm:ss](VIDEO_URL?t=seconds) Topic Title
2. [hh:mm:ss](VIDEO_URL?t=seconds) Topic Title

## Rules
- Only major topic changes
- Titles: 3-6 words, descriptive
- Use timestamps from transcript
- No explanations, just the list

## Transcript:
""",
}


class Summarizer:
    def __init__(self):
        load_dotenv()

    def gemini(self, transcript: str, prompt_type: str = "summary",
               model_type: str = "gemini-2.5-flash", extra: str = "") -> str:
        prompt = PROMPTS.get(prompt_type, PROMPTS["summary"])
        try:
            client = genai.Client(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))
            response = client.models.generate_content(
                model=model_type,
                contents=prompt + extra + transcript
            )
            return response.text
        except Exception as e:
            return f"Gemini error: {e}"

    def openai(self, transcript: str, prompt_type: str = "summary",
               model_type: str = "gpt-5-nano", extra: str = "") -> str:
        prompt = PROMPTS.get(prompt_type, PROMPTS["summary"])
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.responses.create(
                model=model_type,
                input=prompt + extra + transcript
            )
            return response.output_text
        except Exception as e:
            return f"OpenAI error: {e}"

    def summarize(self, transcript: str, prompt_type: str = "summary",
                  provider: str = "gemini") -> str:
        if provider == "openai":
            return self.openai(transcript, prompt_type)
        return self.gemini(transcript, prompt_type)
