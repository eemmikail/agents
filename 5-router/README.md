# Message Router with To-Do List Manager

This project demonstrates a message routing system that can identify tasks and add them to a to-do list.

## Features

- **Message Routing**: Automatically categorizes messages as Tasks, Questions, or Information
- **To-Do List Management**: Manages tasks identified by the router
- **Command-Line Interface**: Provides a CLI for interacting with the to-do list

## Requirements

- Python 3.7+
- Google AI API key (for Gemini model)

## Setup

1. Install the required packages:

   ```
   pip install google-generativeai python-dotenv pydantic
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

If the message is identified as a task, it will be added to your to-do list.

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
3. The `todo_cli.py` provides a command-line interface for interacting with the system.

## File Structure

- `message_routing.py`: Contains the message routing logic
- `todo_manager.py`: Manages the to-do list (add, complete, delete tasks)
- `todo_cli.py`: Command-line interface for the to-do list
- `todos.json`: Storage file for to-do items (created automatically)

## Example

```bash
# Process a message
python todo_cli.py process "Schedule a meeting with the team for tomorrow"

# View your to-do list
python todo_cli.py list
```
