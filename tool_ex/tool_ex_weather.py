from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("GOOGLE_AI_API_KEY")

client = genai.Client(api_key=api_key)

def get_weather(latitude: float, longitude: float) -> dict:
    """
    Retrieves today's temperature data from the Open-Meteo API for the specified coordinates.
    
    Parameters:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.
    
    Returns:
        dict: A dictionary with today's date and min/max temperatures.
              Returns None if the request fails.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "Europe/Istanbul",
        "forecast_days": 1  # Only get today's forecast
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        date = data.get("daily", {}).get("time", [])[0]  # Get today's date
        temp_max = data.get("daily", {}).get("temperature_2m_max", [])[0]
        temp_min = data.get("daily", {}).get("temperature_2m_min", [])[0]
        
        # Format the result
        result = {
            "date": date,
            "max_temperature": temp_max,
            "min_temperature": temp_min
        }
        return result
    else:
        print("API request failed with status code:", response.status_code)
        return None

# Define the function declaration manually
weather_function_declaration = types.FunctionDeclaration(
    name="get_weather",
    description="Retrieves today's temperature data for the specified coordinates",
    parameters={
        "type": "object",
        "properties": {
            "latitude": {
                "type": "number",
                "description": "The latitude of the location"
            },
            "longitude": {
                "type": "number",
                "description": "The longitude of the location"
            }
        },
        "required": ["latitude", "longitude"]
    }
)

# Updated configuration according to the latest Gemini API
# Note: In the latest Gemini API, the function_calling_config should be placed in tool_config
# instead of directly in the Tool object
first_prompt = "What is the weather in Konya?"
model_id = "gemini-2.0-flash"
response = client.models.generate_content(
    contents=[first_prompt],
    model=model_id,
    config=types.GenerateContentConfig(
        tools=[types.Tool(
            function_declarations=[weather_function_declaration]
        )],
        tool_config=types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(
                mode="any",
                allowed_function_names=["get_weather"]
            )
        ),
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False)
    )
) 

# Process the response and handle function calls
print("Response received from Gemini API")

# Check if there are function calls in the response
if hasattr(response.candidates[0].content.parts[0], 'function_call'):
    function_call = response.candidates[0].content.parts[0].function_call
    function_name = function_call.name
    function_args = function_call.args
    
    print(f"Function called: {function_name}")
    print(f"Arguments: {function_args}")
    
    # Execute the function with the provided arguments
    if function_name == "get_weather":
        # Extract latitude and longitude from the arguments
        latitude = function_args.get("latitude")
        longitude = function_args.get("longitude")
        
        # Call the get_weather function
        weather_data = get_weather(latitude, longitude)
        print(f"Weather data: {weather_data}")
        
        # Send the function response back to the model using the correct format
        # Note: In the latest Gemini API, we need to use the types.Content and types.Part classes
        # to structure the conversation history correctly
        follow_up = client.models.generate_content(
            model=model_id,
            contents=[
                types.Content(
                    parts=[types.Part(text=first_prompt)],
                    role="user"
                ),
                types.Content(
                    parts=[types.Part(function_call=function_call)],
                    role="model"
                ),
                types.Content(
                    parts=[types.Part(function_response=types.FunctionResponse(
                        name=function_name,
                        response=weather_data
                    ))],
                    role="function"
                )
            ]
        )
        
        print(f"Final response: {follow_up.text}")
else:
    # If there's no function call, print the text response
    print(f"Text response: {response.text}")