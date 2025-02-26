from google import genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from enum import Enum
from todo_manager import TodoManager
from weather_service import is_weather_question, handle_weather_question

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

def answer_question(question: str) -> str:
    """Use the LLM to answer a general question."""
    prompt = f"""
    Please answer the following question concisely and accurately:
    {question}
    """
    
    response = client.models.generate_content(
        model="gemini-2.0-pro-exp-02-05",
        contents=prompt
    )
    
    return response.text

def process_message(message: str):
    """Process a message by routing it and handling it appropriately."""
    
    # If not a weather question, proceed with normal routing
    routing_result = route_message(message)
    
    if routing_result.result == "Task":
        # If it's a task, add it to the to-do list
        todo_manager = TodoManager()
        todo_item = todo_manager.add_todo(message)
        return f"Added to your to-do list: {todo_item.task} (ID: {todo_item.id})"
    elif routing_result.result == "Question":
        if is_weather_question(message):
            return handle_weather_question(message)
        else:
            # If it's a question, use the LLM to answer it
            return answer_question(message)
    elif routing_result.result == "Information":
        return "Thanks for the information: " + message
    else:
        return "I'm not sure how to handle this message."

# Example usage
if __name__ == "__main__":
    # Test with different types of messages
    print("Question example (weather):")
    print(process_message("What is the weather in Istanbul?"))
    print("\nQuestion example (general):")
    print(process_message("What is the capital of France?"))
    print("\nTask example:")
    print(process_message("Create a proposal for a new product"))
    print("\nInformation example:")
    print(process_message("Tomorrow is your off day"))
    
    # Show current to-do list
    todo_manager = TodoManager()
    print("\nCurrent To-Do List:")
    for todo in todo_manager.get_all_todos():
        status = "✓" if todo.completed else "□"
        print(f"{todo.id}. [{status}] {todo.task}")
