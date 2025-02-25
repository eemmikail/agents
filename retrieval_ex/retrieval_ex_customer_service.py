from google import genai
import os
from dotenv import load_dotenv
import json
from google.genai import types
# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("GOOGLE_AI_API_KEY")

client = genai.Client(api_key=api_key)

def take_a_look_at_the_customer_service_data() -> dict:
    """
    Retrieves customer service data from the data.json file.
    
    Parameters:
        None
    
    Returns:
        dict: A dictionary with customer service data.
    """
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Create the absolute path to data.json
    data_file_path = os.path.join(script_dir, "data.json")
    
    with open(data_file_path, "r") as file:
        data = json.load(file)
    return data

customer_service_function_declaration = types.FunctionDeclaration(
    name="take_a_look_at_the_customer_service_data",
    description="Retrieves customer service data"
)

first_prompt = "Ürünümü iade etmek istiyorum. Nasıl yaparım?"
model_id = "gemini-2.0-flash"
response = client.models.generate_content(
    contents=[first_prompt],
    model=model_id,
    config=types.GenerateContentConfig(
        tools=[types.Tool(
            function_declarations=[customer_service_function_declaration]
        )],
        tool_config=types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(
                mode="any",
                allowed_function_names=["take_a_look_at_the_customer_service_data"]
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

    if function_name == "take_a_look_at_the_customer_service_data":
        customer_service_data = take_a_look_at_the_customer_service_data()
        print(f"Customer service data: {customer_service_data}")

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
                        response=customer_service_data
                    ))],
                    role="function"
                )
            ]
        )
        print(f"Final response: {follow_up.text}")
else:
    # If there's no function call, print the text response
    print(f"Final response: {response.text}")

