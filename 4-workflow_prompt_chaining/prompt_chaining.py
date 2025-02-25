from google import genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import json
import logging
from datetime import datetime
from typing import Optional
# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_AI_API_KEY")
client = genai.Client(api_key=api_key)
model_id = "gemini-2.0-pro-exp-02-05"

class EventExtraction(BaseModel):
    """
    First call to extract event from input text
    """
    description: str = Field(description="The description of the event")
    is_calendar_event: bool = Field(description="Whether the event is a calendar event")
    confidence_score: float = Field(description="The confidence score of the event")

class EventDetails(BaseModel):
    """
    Second call to extract details from the description
    """
    name: str = Field(description="The name of the event")
    date: str = Field(description="The date of the event. Use ISO 8601 format.")
    duration_minutes: int = Field(description="The duration of the event in minutes")
    participants: list[str] = Field(description="The participants of the event")

class EventConfirmation(BaseModel):
    """
    Third call to generate a confirmation message
    """
    confirmation_message: str = Field(description="Natural language confirmation message")

def extract_event_info(text: str) -> EventExtraction:
    """
    Extracts event information from a text.
    """
    print("Starting event extraction")
    print(f"Extracting event information from text: {text}")
    today = datetime.now().strftime('%A, %B %d, %Y')
    prompt = f"""
    Today is {today}.
    Analyze the following text and extract if the text describes a calendar event.
    Text: {text}
    """

    response = client.models.generate_content(
    model=model_id,
    contents=[prompt],
    config={
        "response_mime_type": "application/json",
            "response_schema": EventExtraction
        }
    )
    result = response.parsed
    print(
        f"Extraction complete - Is calendar event: {result.is_calendar_event}, Confidence: {result.confidence_score:.2f}"
    )
    return result

def extract_event_details(description: str) -> EventDetails:
    """
    Extracts event details from a description.
    """
    print("Starting event details extraction")
    print(f"Extracting event details from description: {description}")
    today = datetime.now().strftime('%A, %B %d, %Y')

    prompt = f"""
    Today is {today}. Use this date to understand the references like "tomorrow" or "next week".
    Analyze the following description and extract the event details.
    Description: {description}
    """

    response = client.models.generate_content(
        model=model_id,
        contents=[prompt],
        config={
            "response_mime_type": "application/json",
            "response_schema": EventDetails
        }
    )
    result = response.parsed
    print(
        f"Extraction complete - Name: {result.name}, Date: {result.date}, Duration: {result.duration_minutes}, Participants: {result.participants}"
    )
    return result

def generate_confirmation_message(event_details: EventDetails) -> EventConfirmation:
    """
    Generates a confirmation message for an event.
    """
    print("Starting confirmation message generation")
    print(f"Generating confirmation message for event: {event_details}")

    prompt = f"""
    Generate a natural confirmation message for the event. Sign of with your name; Susie
    <example>
    Dear Ismail,

    I hope this message finds you well. I am pleased to inform you that the event has been accepted. 
    I would like to meet with you at 02-02-2025 at 10:00 to discuss the details further.
    Thank you for your attention, and I look forward to our meeting.
    Best regards,

    Susie
    </example>
    Use the example but be creative about details.
    Event Details: {event_details.model_dump()}
    """

    completion = client.models.generate_content(
        model=model_id,
        contents=[prompt],
        config={
            "response_mime_type": "application/json",
            "response_schema": EventConfirmation
        }
    )
    result = completion.parsed
    print(
        f"Confirmation message generated: {result.confirmation_message}"
    )
    return result

def process_event_request(text: str) -> Optional[EventConfirmation]:
    """
    Processes an event request and returns a confirmation message.
    """
    print("Processing event request")
    print(f"Processing event request: {text}")

    event_check = extract_event_info(text)
    if (
        not event_check.is_calendar_event
        or event_check.confidence_score < 0.7
    ):
        print("Gatekeeping: Event is not a calendar event or confidence score is too low")
        return None
    
    print("Event is a calendar event, extracting details")

    event_details = extract_event_details(event_check.description)

    confirmation = generate_confirmation_message(event_details)

    print("Confirmation message generated successfully")
    return confirmation

appropriate_user_input = "I have a meeting with John tomorrow at 10am for 2 hours"

confirmation = process_event_request(appropriate_user_input)

unappropriate_user_input = "Can you tell me about the weather in Tokyo?"

unappropriate_confirmation = process_event_request(unappropriate_user_input)




