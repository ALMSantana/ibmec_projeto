from __future__ import annotations

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-nano")
PERSONA_MODEL = os.getenv("PERSONA_MODEL", "gpt-3.5-turbo-0125")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))