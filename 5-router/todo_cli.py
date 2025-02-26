from message_routing import process_message
from todo_manager import TodoManager
import argparse

def display_todos(todos):
    """Display a list of todos in a formatted way."""
    if not todos:
        print("No items in the to-do list.")
        return
    
    for todo in todos:
        status = "✓" if todo.completed else "□"
        created = todo.created_at.strftime("%Y-%m-%d %H:%M")
        completed = todo.completed_at.strftime("%Y-%m-%d %H:%M") if todo.completed_at else "N/A"
        print(f"{todo.id}. [{status}] {todo.task}")
        print(f"   Created: {created} | Completed: {completed}")

def main():
    parser = argparse.ArgumentParser(description="To-Do List Manager")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Add a new task
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("task", help="Task description")
    
    # Complete a task
    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    complete_parser.add_argument("id", type=int, help="Task ID to complete")
    
    # Delete a task
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID to delete")
    
    # List tasks
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--all", action="store_true", help="Show all tasks")
    list_parser.add_argument("--completed", action="store_true", help="Show only completed tasks")
    
    # Process a message (auto-route)
    process_parser = subparsers.add_parser("process", help="Process a message and route it")
    process_parser.add_argument("message", help="Message to process")
    
    args = parser.parse_args()
    todo_manager = TodoManager()
    
    if args.command == "add":
        todo = todo_manager.add_todo(args.task)
        print(f"Added task: {todo.task} (ID: {todo.id})")
    
    elif args.command == "complete":
        todo = todo_manager.complete_todo(args.id)
        if todo:
            print(f"Marked task as completed: {todo.task}")
        else:
            print(f"No task found with ID {args.id}")
    
    elif args.command == "delete":
        success = todo_manager.delete_todo(args.id)
        if success:
            print(f"Deleted task with ID {args.id}")
        else:
            print(f"No task found with ID {args.id}")
    
    elif args.command == "list":
        if args.completed:
            print("Completed Tasks:")
            display_todos(todo_manager.get_completed_todos())
        elif args.all:
            print("All Tasks:")
            display_todos(todo_manager.get_all_todos())
        else:
            print("Active Tasks:")
            display_todos(todo_manager.get_active_todos())
    
    elif args.command == "process":
        result = process_message(args.message)
        print(result)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 