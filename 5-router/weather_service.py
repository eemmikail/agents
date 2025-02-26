import requests
from typing import Optional, Dict, Any
import re

def extract_location(question: str) -> Optional[str]:
    """Extract location from a weather-related question."""
    # Simple pattern to extract location from weather questions
    patterns = [
        r"weather\s+in\s+([A-Za-z\s]+)(?:\?|$)",
        r"temperature\s+in\s+([A-Za-z\s]+)(?:\?|$)",
        r"how\s+(?:hot|cold|warm)\s+is\s+(?:it\s+in\s+)?([A-Za-z\s]+)(?:\?|$)",
        r"what'?s\s+the\s+weather\s+(?:like\s+)?(?:in\s+)?([A-Za-z\s]+)(?:\?|$)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, question, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None

def geocode_location(location: str) -> Optional[Dict[str, float]]:
    """Convert location name to latitude and longitude."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "WeatherApp/1.0"  # Required by Nominatim's ToS
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return {
                    "latitude": float(data[0]["lat"]),
                    "longitude": float(data[0]["lon"]),
                    "display_name": data[0]["display_name"]
                }
    except Exception as e:
        print(f"Error geocoding location: {e}")
    
    return None

def get_weather(latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
    """
    Retrieves today's temperature data from the Open-Meteo API for the specified coordinates.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
        "forecast_days": 1  # Only get today's forecast
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            date = data.get("daily", {}).get("time", [])[0]  # Get today's date
            temp_max = data.get("daily", {}).get("temperature_2m_max", [])[0]
            temp_min = data.get("daily", {}).get("temperature_2m_min", [])[0]
            precipitation = data.get("daily", {}).get("precipitation_sum", [])[0]
            
            # Format the result
            result = {
                "date": date,
                "max_temperature": temp_max,
                "min_temperature": temp_min,
                "precipitation": precipitation,
                "units": {
                    "temperature": data.get("daily_units", {}).get("temperature_2m_max", "°C"),
                    "precipitation": data.get("daily_units", {}).get("precipitation_sum", "mm")
                }
            }
            return result
        else:
            print(f"Weather API request failed with status code: {response.status_code}")
    except Exception as e:
        print(f"Error getting weather data: {e}")
    
    return None

def is_weather_question(question: str) -> bool:
    """Determine if a question is asking about weather."""
    weather_keywords = [
        "weather", "temperature", "hot", "cold", "warm", "rain", "sunny", 
        "forecast", "climate", "humidity", "precipitation"
    ]
    
    question_lower = question.lower()
    return any(keyword in question_lower for keyword in weather_keywords)

def get_weather_for_location(location: str) -> Optional[Dict[str, Any]]:
    """Get weather for a specific location."""
    geo_data = geocode_location(location)
    if geo_data:
        weather_data = get_weather(geo_data["latitude"], geo_data["longitude"])
        if weather_data:
            weather_data["location"] = geo_data["display_name"]
            return weather_data
    return None

def format_weather_response(weather_data: Dict[str, Any]) -> str:
    """Format weather data into a human-readable response."""
    location = weather_data.get("location", "the requested location")
    date = weather_data.get("date", "today")
    max_temp = weather_data.get("max_temperature")
    min_temp = weather_data.get("min_temperature")
    precipitation = weather_data.get("precipitation")
    temp_unit = weather_data.get("units", {}).get("temperature", "°C")
    precip_unit = weather_data.get("units", {}).get("precipitation", "mm")
    
    response = f"Weather for {location} on {date}:\n"
    response += f"- Maximum temperature: {max_temp}{temp_unit}\n"
    response += f"- Minimum temperature: {min_temp}{temp_unit}\n"
    response += f"- Precipitation: {precipitation}{precip_unit}"
    
    return response

def handle_weather_question(question: str) -> str:
    """Process a weather-related question and return a response."""
    location = extract_location(question)
    
    if not location:
        return "I couldn't determine which location you're asking about. Please specify a city or region."
    
    weather_data = get_weather_for_location(location)
    
    if weather_data:
        return format_weather_response(weather_data)
    else:
        return f"Sorry, I couldn't retrieve weather information for {location}. Please try another location."

# Example usage
if __name__ == "__main__":
    test_questions = [
        "What is the weather in Tokyo?",
        "How hot is it in New York?",
        "Tell me the temperature in Paris",
        "Is it raining in London?"
    ]
    
    for question in test_questions:
        print(f"Question: {question}")
        if is_weather_question(question):
            print(f"Response: {handle_weather_question(question)}")
        else:
            print("Not a weather question")
        print() 