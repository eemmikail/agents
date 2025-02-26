from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
import json
import os

class TodoItem(BaseModel):
    id: int
    task: str
    created_at: datetime = Field(default_factory=datetime.now)
    completed: bool = False
    completed_at: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class TodoManager:
    def __init__(self, storage_file: str = "todos.json"):
        self.storage_file = storage_file
        self.todos: List[TodoItem] = []
        self.load_todos()
    
    def load_todos(self):
        """Load todos from the storage file if it exists."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r") as f:
                    todos_data = json.load(f)
                    self.todos = []
                    for todo_data in todos_data:
                        # Convert string dates back to datetime objects
                        if "created_at" in todo_data and todo_data["created_at"]:
                            todo_data["created_at"] = datetime.fromisoformat(todo_data["created_at"])
                        if "completed_at" in todo_data and todo_data["completed_at"]:
                            todo_data["completed_at"] = datetime.fromisoformat(todo_data["completed_at"])
                        self.todos.append(TodoItem(**todo_data))
            except Exception as e:
                print(f"Error loading todos: {e}")
                self.todos = []
    
    def save_todos(self):
        """Save todos to the storage file."""
        try:
            with open(self.storage_file, "w") as f:
                todos_json = [todo.dict() for todo in self.todos]
                json.dump(todos_json, f, default=str, indent=2)
        except Exception as e:
            print(f"Error saving todos: {e}")
    
    def add_todo(self, task: str) -> TodoItem:
        """Add a new todo item."""
        # Generate a new ID (simple increment)
        new_id = 1 if not self.todos else max(todo.id for todo in self.todos) + 1
        
        # Create new todo item
        todo = TodoItem(id=new_id, task=task)
        self.todos.append(todo)
        self.save_todos()
        return todo
    
    def complete_todo(self, todo_id: int) -> Optional[TodoItem]:
        """Mark a todo as completed."""
        for todo in self.todos:
            if todo.id == todo_id:
                todo.completed = True
                todo.completed_at = datetime.now()
                self.save_todos()
                return todo
        return None
    
    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo item."""
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                del self.todos[i]
                self.save_todos()
                return True
        return False
    
    def get_all_todos(self) -> List[TodoItem]:
        """Get all todo items."""
        return self.todos
    
    def get_active_todos(self) -> List[TodoItem]:
        """Get all active (not completed) todo items."""
        return [todo for todo in self.todos if not todo.completed]
    
    def get_completed_todos(self) -> List[TodoItem]:
        """Get all completed todo items."""
        return [todo for todo in self.todos if todo.completed]

# Example usage
if __name__ == "__main__":
    todo_manager = TodoManager()
    todo_manager.add_todo("Buy groceries")
    todo_manager.add_todo("Finish project report")
    print("All todos:", todo_manager.get_all_todos()) 