from google import genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from enum import Enum

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("GOOGLE_AI_API_KEY")

client = genai.Client(api_key=api_key)

class RoutingResult(Enum):
    TASK = "Task"
    QUESTION = "Question"
    INFORMATION = "Information"

class MessageForRouting(BaseModel):
    # result of the routing as enum like ["Task", "Question", "Information"]
    result: RoutingResult = Field(description="The result of the routing, ['Task', 'Question', 'Information']")
    class Config:
        use_enum_values = True

def route_message(message: str) -> MessageForRouting:
    prompt = f"""
    You are a helpful assistant that routes messages to the appropriate destination.
    The possible destinations are:
    - Task
    - Question
    - Information
    The message is: {message}
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
        "response_mime_type": "application/json",
            "response_schema": MessageForRouting
        }
    )
    return response.parsed

routing_result = route_message("What is the weather in Tokyo?")
print(routing_result.result)

routing_result = route_message("Can you create a proposal for a new product?")
print(routing_result.result)

routing_result = route_message("Tomorrow is your off day")
print(routing_result.result)
