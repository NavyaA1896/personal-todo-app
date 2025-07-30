import json

class Task:
    def __init__(self, title, description, category):
        self.title = title
        self.description = description
        self.category = category
        self.completed = False

    def mark_completed(self):
        self.completed = True

def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump([task.__dict__ for task in tasks], f, indent=4)

def load_tasks():
    try:
        with open('tasks.json', 'r') as f:
            return [Task(**data) for data in json.load(f)]
    except FileNotFoundError:
        return []

def display_tasks(tasks):
    if not tasks:
        print("\nNo tasks available.\n")
        return
    print("\nYour Tasks:")
    for i, task in enumerate(tasks):
        status = "✓" if task.completed else "✗"
        print(f"{i + 1}. [{status}] {task.title} ({task.category}) - {task.description}")

def main():
    tasks = load_tasks()
    while True:
        print("\n==== TO-DO LIST MENU ====")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task Completed")
        print("4. Delete Task")
        print("5. Edit Task")
        print("6. Exit")


        choice = input("Choose an option: ")
        
        if choice == '1':
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            category = input("Enter task category (e.g., Work, Personal): ")
            tasks.append(Task(title, description, category))
            print("✅ Task added successfully!")

        elif choice == '2':
            display_tasks(tasks)

        elif choice == '3':
            display_tasks(tasks)
            try:
                idx = int(input("Enter task number to mark as completed: ")) - 1
                if 0 <= idx < len(tasks):
                    tasks[idx].mark_completed()
                    print("✅ Task marked as completed.")
                else:
                    print("❌ Invalid task number.")
            except ValueError:
                print("❌ Please enter a valid number.")

        elif choice == '4':
            display_tasks(tasks)
            try:
                idx = int(input("Enter task number to delete: ")) - 1
                if 0 <= idx < len(tasks):
                    deleted = tasks.pop(idx)
                    print(f"🗑️ Deleted task: {deleted.title}")
                else:
                    print("❌ Invalid task number.")
            except ValueError:
                print("❌ Please enter a valid number.")

        elif choice == '5':
            display_tasks(tasks)
            try:
                idx = int(input("Enter task number to edit: ")) - 1
                if 0 <= idx < len(tasks):
                    task = tasks[idx]
                    print(f"Editing: {task.title}")
                    new_title = input(f"New title (press Enter to keep '{task.title}'): ")
                    new_desc = input(f"New description (press Enter to keep '{task.description}'): ")
                    new_cat = input(f"New category (press Enter to keep '{task.category}'): ")

                    if new_title.strip(): task.title = new_title
                    if new_desc.strip(): task.description = new_desc
                    if new_cat.strip(): task.category = new_cat

                    print("✅ Task updated successfully.")
                else:
                    print("❌ Invalid task number.")
            except ValueError:
                print("❌ Please enter a valid number.")
        elif choice == '6':
            save_tasks(tasks)
            print("👋 Exiting. Tasks saved successfully.")
            break


        else:
            print("❌ Invalid choice. Please select a number between 1 and 5.")

if __name__ == "__main__":
    main()
