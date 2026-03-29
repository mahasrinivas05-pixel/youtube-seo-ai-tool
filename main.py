# main.py

import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def generate_ai_content(concept, keywords, title, description):

    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    prompt = f"""
You are a YouTube SEO + Content Expert.

INPUT:
Concept of Video:
{concept}

Keywords:
{keywords}

Current Title:
{title}

Current Description:
{description}

YOUR TASK:

1. Improve the content (DO NOT keyword stuff)

2. Generate 3 BETTER titles:
- Length: 40–60 characters
- Use keywords naturally (NOT all)
- Must be human readable
- Add curiosity + hook (What if, Secret, Shocking, etc.)
- Avoid robotic keyword stuffing

3. Generate 1 optimized description:
- Length: 250–350 characters
- Must include most keywords naturally
- Add storytelling tone
- Add hashtags at end

4. Keep it HIGH CTR + NATURAL (very important)

STRICT FORMAT:

Title 1: ...
Title 2: ...
Title 3: ...

Description:
...

Hashtags:
...
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text