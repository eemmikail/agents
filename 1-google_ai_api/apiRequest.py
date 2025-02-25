from google import genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import json

class EnglishAdjectives(BaseModel):
    word: str
    definition: str
    example: str

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("GOOGLE_AI_API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-pro-exp-02-05",
    contents="Generate 10 English adjectives with their definitions and examples",
    config={
        "response_mime_type": "application/json",
        "response_schema": list[EnglishAdjectives]
    }
)
print(response.parsed[0])
