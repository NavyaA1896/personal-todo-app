import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# ----- Task Class -----
class Task:
    def __init__(self, title, description, category, completed=False):
        self.title = title
        self.description = description
        self.category = category
        self.completed = completed

    def mark_completed(self):
        self.completed = True

# ----- File Handling -----
def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump([task.__dict__ for task in tasks], f, indent=4)

def load_tasks():
    if not os.path.exists('tasks.json'):
        return []
    with open('tasks.json', 'r') as f:
        return [Task(**data) for data in json.load(f)]

# ----- Main App Class -----
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.tasks = load_tasks()

        # UI Elements
        self.listbox = tk.Listbox(root, width=60, height=10)
        self.listbox.pack(pady=10)

        tk.Button(root, text="Add Task", command=self.add_task).pack()
        tk.Button(root, text="Mark Completed", command=self.mark_completed).pack()
        tk.Button(root, text="Delete Task", command=self.delete_task).pack()
        tk.Button(root, text="Edit Task", command=self.edit_task).pack()

        self.status_label = tk.Label(root, text="", fg="green")
        self.status_label.pack()

        self.refresh_listbox()

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✓" if task.completed else "✗"
            self.listbox.insert(tk.END, f"[{status}] {task.title} ({task.category}) - {task.description}")

    def add_task(self):
        title = simpledialog.askstring("Add Task", "Enter title:")
        if not title: return
        desc = simpledialog.askstring("Add Task", "Enter description:")
        cat = simpledialog.askstring("Add Task", "Enter category:")
        self.tasks.append(Task(title, desc, cat))
        save_tasks(self.tasks)
        self.refresh_listbox()
        self.status_label.config(text="✅ Task added successfully")

    def mark_completed(self):
        idx = self.listbox.curselection()
        if not idx:
            messagebox.showwarning("Select Task", "Please select a task to mark as completed.")
            return
        self.tasks[idx[0]].mark_completed()
        save_tasks(self.tasks)
        self.refresh_listbox()
        self.status_label.config(text="✅ Task marked as completed")

    def delete_task(self):
        idx = self.listbox.curselection()
        if not idx:
            messagebox.showwarning("Select Task", "Please select a task to delete.")
            return
        task = self.tasks.pop(idx[0])
        save_tasks(self.tasks)
        self.refresh_listbox()
        self.status_label.config(text=f"🗑️ Deleted task: {task.title}")

    def edit_task(self):
        idx = self.listbox.curselection()
        if not idx:
            messagebox.showwarning("Select Task", "Please select a task to edit.")
            return
        task = self.tasks[idx[0]]
        new_title = simpledialog.askstring("Edit Task", f"New title (leave blank to keep '{task.title}'):")
        new_desc = simpledialog.askstring("Edit Task", f"New description (leave blank to keep '{task.description}'):")
        new_cat = simpledialog.askstring("Edit Task", f"New category (leave blank to keep '{task.category}'):")

        if new_title: task.title = new_title
        if new_desc: task.description = new_desc
        if new_cat: task.category = new_cat

        save_tasks(self.tasks)
        self.refresh_listbox()
        self.status_label.config(text="✅ Task updated successfully")

# ----- Run App -----
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
