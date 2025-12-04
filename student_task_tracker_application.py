# ------------------------------------------------------------------------------------------------------------------
#                                                   ASSIGNMENT
#                                                      ON
#                                      "STUDENT TASK TRACKER APPLICATION"
# ------------------------------------------------------------------------------------------------------------------
#         Project Title : Student Task Tracker Application
#         Module 6 Assignment Topic : OOP, Functions, File Handling, JSON, Modules, Error Handling and Datetime.
#         Course Name : Full Stack Web Development with Python, Django & React
#         Batch : 8
#         Institution Name : OSTAD
#                 
# 
#         This project covers:

#            ✔ Object-Oriented Programming (OOP)

#            ✔ Classes & Methods

#            ✔ File Handling (Read & Write operations)

#            ✔ JSON Data Storage

#            ✔ Error Handling (try–except)

#            ✔ Datetime Module

#            ✔ Python Modules (random, uuid)

#            ✔ Menu-driven CLI Application

#            ✔ CRUD Operations (Add, View, Update, Delete Tasks)

# ------------------------------------------------------------------------------------------------------------------
#                                            ASSIGNMENT SUBMISSION
#                                       ------------------------------
#                             
#                                               Submitted To

#                                             OSTAD Instructor



#                                               Submitted By

#                                         Name: Md. Ahosanul Kabir
#                                         Phone: 01762007433
#                                         Email: akl279f@gmail.com


#                                       Submission Date: 5/12/2025
# ------------------------------------------------------------------------------------------------------------------

import json
import os
import sys
import uuid
from datetime import datetime
import signal
import random


# ===============================================================
# CLASS: Task  (Represents a single task)
# ===============================================================
class Task:
    def __init__(self, title: str, description: str, created_at: str = None, id: str = None):
        self.id = id or Task.generate_id()
        self.title = title
        self.description = description
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def generate_id():
        return f"{uuid.uuid4().hex}-{random.randint(100,999)}"

    def to_dict(self):
        """Return serializable dict representation of the task."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create a Task object from a dict (loaded from JSON)."""
        return cls(
            id=data.get("id"),
            title=data.get("title", ""),
            description=data.get("description", ""),
            created_at=data.get("created_at")
        )
    
# ===============================================================
# CLASS: TaskManager (Handles CRUD + File + Error Handling)
# ===============================================================
class TaskManager:
    def __init__(self, file_path="tasks.json"):
        self.file_path = file_path
        self.tasks = []   # list of Task objects
        self.load_from_file()

        signal.signal(signal.SIGINT, self._signal_handler)

    # ---------------- FILE HANDLING ----------------
    def load_from_file(self):
        """Load tasks safely from JSON file."""
        if not os.path.exists(self.file_path):
            self.tasks = []
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    self.tasks = [Task.from_dict(item) for item in data]
                else:
                    print("Warning: Invalid file format. Starting with empty list.")
                    self.tasks = []

        except json.JSONDecodeError:
            print("Error: tasks.json corrupted. Starting fresh.")
            self.tasks = []
        except Exception as e:
            print(f"Unexpected error while loading: {e}")
            self.tasks = []

    def save_to_file(self):
        """Write tasks to JSON with error handling."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([t.to_dict() for t in self.tasks], f, indent=4, ensure_ascii=False)
            print(f"Saved {len(self.tasks)} task(s).")
        except Exception as e:
            print(f"Error while saving: {e}")


    
    # ---------------- CRUD OPERATIONS ----------------
    def add_task(self, title: str, description: str):
        """Add a new task to the list."""
        task = Task(title=title.strip(), description=description.strip())
        self.tasks.append(task)
        print(f"Task added successfully! (ID: {task.id})")

       
    def view_tasks(self):
        """Display all tasks nicely."""
        if not self.tasks:
            print("\nNo tasks found.\n")
            return

        print("\n========== All Tasks ==========")
        for i, t in enumerate(self.tasks, start=1):
            print(f"{i}. ID: {t.id}")
            print(f"   Title      : {t.title}")
            print(f"   Description: {t.description}")
            print(f"   Created At : {t.created_at}")
            print("--------------------------------")
        print("")

    def find_task_index_by_id(self, task_id: str):
        """Find task index or raise ValueError."""
        for i, t in enumerate(self.tasks):
            if t.id == task_id:
                return i
        raise ValueError("Task ID not found.")

    def update_task(self, task_id: str, new_title=None, new_description=None):
        try:
            idx = self.find_task_index_by_id(task_id)

            if new_title and new_title.strip():
                self.tasks[idx].title = new_title.strip()
            if new_description and new_description.strip():
                self.tasks[idx].description = new_description.strip()

            print("Task updated successfully.")
        except ValueError as e:
            print(f"Update failed: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def delete_task(self, task_id: str):
        try:
            idx = self.find_task_index_by_id(task_id)
            removed = self.tasks.pop(idx)
            print(f"Task deleted! (ID: {removed.id})")
        except ValueError as e:
            print(f"Delete failed: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    # ---------------- UTILITIES ----------------
    def list_tasks_brief(self):
        if not self.tasks:
            print("No tasks available.")
            return
        for i, t in enumerate(self.tasks, start=1):
            print(f"{i}. {t.title} (ID: {t.id})")

    def _signal_handler(self, signum, frame):
        print("\nCtrl+C detected. Saving and exiting...")
        self.save_to_file()
        sys.exit(0)


# ===============================================================
# HELPER INPUT FUNCTIONS
# ===============================================================
def input_non_empty(msg):
    """Ask user until non-empty value is provided."""
    while True:
        val = input(msg).strip()
        if val:
            return val
        print("Input cannot be empty.")

def input_choice(msg, choices):
    """Ensure choice is valid."""
    while True:
        val = input(msg).strip()
        if val in choices:
            return val
        print(f"Choose one of {choices}")


# ===============================================================
# MAIN MENU LOGIC
# ===============================================================
def main():
    manager = TaskManager()

    menu = """
==============================
 Student Task Tracker Application
==============================
1. Add New Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Exit
"""

    while True:
        print(menu)
        choice = input_choice("Enter choice (1-5): ", ("1", "2", "3", "4", "5"))

        if choice == "1":
            print("\n--- Add New Task ---")
            title = input_non_empty("Task Title: ")
            description = input_non_empty("Description: ")
            manager.add_task(title, description)

        elif choice == "2":
            print("\n--- Task List ---")
            manager.view_tasks()

        elif choice == "3":
            print("\n--- Update Task ---")
            if not manager.tasks:
                print("No tasks available.")
                continue
            manager.list_tasks_brief()
            t_id = input_non_empty("Enter Task ID to update: ")

            new_title = input("New Title (leave blank to keep): ")
            new_desc = input("New Description (leave blank to keep): ")

            manager.update_task(
                t_id,
                new_title if new_title.strip() else None,
                new_desc if new_desc.strip() else None
            )

        elif choice == "4":
            print("\n--- Delete Task ---")
            if not manager.tasks:
                print("No tasks available.")
                continue

            manager.list_tasks_brief()
            t_id = input_non_empty("Enter Task ID to delete: ")
            confirm = input_choice("Delete? (y/n): ", ("y", "n"))
            if confirm == "y":
                manager.delete_task(t_id)

        elif choice == "5":
            print("\nSaving tasks and exiting...")
            manager.save_to_file()
            print("Goodbye!")
            break


# ENTRY POINT
if __name__ == "__main__":
    main()