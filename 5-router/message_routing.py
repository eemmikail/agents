from google import genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from enum import Enum
from todo_manager import TodoManager

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

def process_message(message: str):
    """Process a message by routing it and handling it appropriately."""
    routing_result = route_message(message)
    
    if routing_result.result == "Task":
        # If it's a task, add it to the to-do list
        todo_manager = TodoManager()
        todo_item = todo_manager.add_todo(message)
        return f"Added to your to-do list: {todo_item.task} (ID: {todo_item.id})"
    elif routing_result.result == "Question":
        return "I'll try to answer your question: " + message
    elif routing_result.result == "Information":
        return "Thanks for the information: " + message
    else:
        return "I'm not sure how to handle this message."

# Example usage
if __name__ == "__main__":
    # Test with different types of messages
    print(process_message("What is the weather in Tokyo?"))
    print(process_message("Can you create a proposal for a new product?"))
    print(process_message("Tomorrow is your off day"))
    
    # Additional task examples
    print(process_message("Buy groceries for dinner"))
    print(process_message("Call John about the project"))
    
    # Show current to-do list
    todo_manager = TodoManager()
    print("\nCurrent To-Do List:")
    for todo in todo_manager.get_all_todos():
        status = "✓" if todo.completed else "□"
        print(f"{todo.id}. [{status}] {todo.task}")
