# Smart Assistant with Message Router

This project demonstrates a smart assistant system that can:

1. Route messages to appropriate handlers (tasks, questions, information)
2. Manage a to-do list for tasks
3. Answer weather questions with real-time data
4. Answer general questions using an LLM

## Features

- **Message Routing**: Automatically categorizes messages as Tasks, Questions, or Information
- **To-Do List Management**: Manages tasks identified by the router
- **Weather Information**: Provides real-time weather data for locations worldwide
- **Question Answering**: Uses Gemini AI to answer general questions
- **Command-Line Interface**: Provides a CLI for interacting with all features

## Requirements

- Python 3.7+
- Google AI API key (for Gemini model)
- Internet connection (for weather data)

## Setup

1. Install the required packages:

   ```
   pip install google-generativeai python-dotenv pydantic requests
   ```

2. Create a `.env` file in the project directory with your Google AI API key:
   ```
   GOOGLE_AI_API_KEY=your_api_key_here
   ```

## Usage

### Message Processing

Process a message and let the system automatically route it:

```bash
python todo_cli.py process "Buy groceries for dinner"
```

The system will:

- Add it to your to-do list if it's a task
- Provide weather information if it's a weather question
- Answer it using the LLM if it's a general question
- Acknowledge it if it's just information

### Weather Information

Get weather information directly:

```bash
python todo_cli.py weather "Tokyo"
```

### Ask Questions

Ask a question directly:

```bash
python todo_cli.py ask "What is the capital of France?"
```

### To-Do List Management

Add a task directly:

```bash
python todo_cli.py add "Complete the project report"
```

List all active tasks:

```bash
python todo_cli.py list
```

List all tasks (including completed):

```bash
python todo_cli.py list --all
```

List only completed tasks:

```bash
python todo_cli.py list --completed
```

Mark a task as completed:

```bash
python todo_cli.py complete 1
```

Delete a task:

```bash
python todo_cli.py delete 1
```

## How It Works

1. The `message_routing.py` file contains the logic to categorize messages using the Gemini AI model.
2. When a message is identified as a task, it's added to the to-do list managed by `todo_manager.py`.
3. Weather questions are detected and handled by `weather_service.py`, which uses the Open-Meteo API.
4. General questions are answered by the Gemini AI model.
5. The `todo_cli.py` provides a command-line interface for interacting with the system.

## File Structure

- `message_routing.py`: Contains the message routing logic
- `todo_manager.py`: Manages the to-do list (add, complete, delete tasks)
- `weather_service.py`: Handles weather-related questions and API calls
- `todo_cli.py`: Command-line interface for the entire system
- `todos.json`: Storage file for to-do items (created automatically)

## Examples

```bash
# Process a weather question
python todo_cli.py process "What's the weather in London?"

# Process a task
python todo_cli.py process "Schedule a meeting with the team for tomorrow"

# Process a general question
python todo_cli.py process "What is the tallest mountain in the world?"

# Get weather directly
python todo_cli.py weather "Paris"

# View your to-do list
python todo_cli.py list
```
