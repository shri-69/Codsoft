import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import sys

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Set application icon (if available)
        try:
            self.root.iconbitmap('todo.ico')
        except:
            pass
        
        # Variables
        self.tasks = []
        self.filter_status = "All"  # All, Pending, Completed
        self.filename = "tasks.json"
        
        # Load tasks from file
        self.load_tasks()
        
        # Configure styles
        self.configure_styles()
        
        # Create GUI
        self.create_widgets()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def configure_styles(self):
        """Configure custom styles for the application"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors
        self.bg_color = '#f0f0f0'
        self.primary_color = '#4a6fa5'
        self.secondary_color = '#166088'
        self.accent_color = '#ff7e5f'
        self.completed_color = '#d4edda'
        self.pending_color = '#fff3cd'
        
        # Configure Treeview style
        self.style.configure("Treeview",
                            background="white",
                            foreground="black",
                            rowheight=25,
                            fieldbackground="white")
        self.style.map('Treeview', background=[('selected', '#347083')])

    def create_widgets(self):
        """Create all GUI widgets"""
        # Title Frame
        title_frame = tk.Frame(self.root, bg=self.primary_color, height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, 
                              text="📝 To-Do List Manager",
                              font=("Arial", 24, "bold"),
                              bg=self.primary_color,
                              fg="white")
        title_label.pack(pady=20)
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Input Frame
        input_frame = tk.Frame(main_container, bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(input_frame, 
                text="Add New Task:", 
                font=("Arial", 12, "bold"),
                bg=self.bg_color).pack(anchor=tk.W)
        
        # Task input
        self.task_var = tk.StringVar()
        task_entry = tk.Entry(input_frame, 
                            textvariable=self.task_var,
                            font=("Arial", 12),
                            width=50,
                            bd=2,
                            relief=tk.GROOVE)
        task_entry.pack(side=tk.LEFT, padx=(0, 10))
        task_entry.bind("<Return>", lambda e: self.add_task())
        
        # Priority selection
        tk.Label(input_frame, 
                text="Priority:", 
                font=("Arial", 11),
                bg=self.bg_color).pack(side=tk.LEFT, padx=(10, 5))
        
        self.priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(input_frame,
                                    textvariable=self.priority_var,
                                    values=["High", "Medium", "Low"],
                                    state="readonly",
                                    width=10)
        priority_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Due date
        tk.Label(input_frame, 
                text="Due Date (YYYY-MM-DD):", 
                font=("Arial", 11),
                bg=self.bg_color).pack(side=tk.LEFT, padx=(10, 5))
        
        self.due_date_var = tk.StringVar()
        due_date_entry = tk.Entry(input_frame,
                                textvariable=self.due_date_var,
                                font=("Arial", 11),
                                width=15)
        due_date_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Add button
        add_btn = tk.Button(input_frame,
                          text="➕ Add Task",
                          command=self.add_task,
                          bg=self.accent_color,
                          fg="white",
                          font=("Arial", 11, "bold"),
                          padx=15,
                          pady=5,
                          bd=0,
                          cursor="hand2")
        add_btn.pack(side=tk.LEFT)
        
        # Filter Frame
        filter_frame = tk.Frame(main_container, bg=self.bg_color)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(filter_frame,
                text="Filter Tasks:",
                font=("Arial", 11, "bold"),
                bg=self.bg_color).pack(side=tk.LEFT)
        
        filter_options = ["All", "Pending", "Completed", "High Priority", "Today"]
        for option in filter_options:
            btn = tk.Button(filter_frame,
                          text=option,
                          command=lambda opt=option: self.filter_tasks(opt),
                          bg=self.secondary_color if option == "All" else self.primary_color,
                          fg="white",
                          font=("Arial", 10),
                          padx=10,
                          pady=3,
                          bd=0,
                          cursor="hand2")
            btn.pack(side=tk.LEFT, padx=5)
        
        # Task List Frame
        list_frame = tk.Frame(main_container, bg=self.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview for tasks
        columns = ("Status", "Task", "Priority", "Due Date", "Created")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Define headings
        self.tree.heading("Status", text="Status")
        self.tree.heading("Task", text="Task")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Created", text="Created")
        
        # Define columns
        self.tree.column("Status", width=80, anchor=tk.CENTER)
        self.tree.column("Task", width=300, anchor=tk.W)
        self.tree.column("Priority", width=100, anchor=tk.CENTER)
        self.tree.column("Due Date", width=100, anchor=tk.CENTER)
        self.tree.column("Created", width=120, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click event
        self.tree.bind("<Double-1>", self.on_task_double_click)
        
        # Action Buttons Frame
        action_frame = tk.Frame(main_container, bg=self.bg_color)
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Action buttons
        actions = [
            ("✅ Mark Complete", self.mark_complete, "#28a745"),
            ("✏️ Edit Task", self.edit_task, "#17a2b8"),
            ("🗑️ Delete Task", self.delete_task, "#dc3545"),
            ("📊 Statistics", self.show_statistics, "#6c757d"),
            ("💾 Save & Exit", self.save_and_exit, "#343a40")
        ]
        
        for text, command, color in actions:
            btn = tk.Button(action_frame,
                          text=text,
                          command=command,
                          bg=color,
                          fg="white",
                          font=("Arial", 10, "bold"),
                          padx=15,
                          pady=8,
                          bd=0,
                          cursor="hand2")
            btn.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_bar = tk.Label(self.root,
                                 text=f"Total Tasks: {len(self.tasks)} | "
                                      f"Pending: {self.count_pending()} | "
                                      f"Completed: {self.count_completed()}",
                                 bd=1,
                                 relief=tk.SUNKEN,
                                 anchor=tk.W,
                                 bg=self.primary_color,
                                 fg="white",
                                 font=("Arial", 10))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Load tasks into treeview
        self.refresh_task_list()

    def add_task(self):
        """Add a new task to the list"""
        task_text = self.task_var.get().strip()
        if not task_text:
            messagebox.showwarning("Warning", "Please enter a task description!")
            return
        
        priority = self.priority_var.get()
        due_date = self.due_date_var.get().strip()
        
        # Validate date format
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                return
        
        task = {
            "id": len(self.tasks) + 1,
            "task": task_text,
            "priority": priority,
            "due_date": due_date,
            "status": "Pending",
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "completed_date": None
        }
        
        self.tasks.append(task)
        self.refresh_task_list()
        
        # Clear input fields
        self.task_var.set("")
        self.due_date_var.set("")
        
        # Update status bar
        self.update_status_bar()
        
        messagebox.showinfo("Success", "Task added successfully!")

    def mark_complete(self):
        """Mark selected task as complete"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to mark as complete!")
            return
        
        for item in selected:
            task_id = int(self.tree.item(item)['values'][0])
            for task in self.tasks:
                if task["id"] == task_id:
                    if task["status"] == "Pending":
                        task["status"] = "Completed"
                        task["completed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    else:
                        task["status"] = "Pending"
                        task["completed_date"] = None
        
        self.refresh_task_list()
        self.update_status_bar()
        self.save_tasks()

    def edit_task(self):
        """Edit selected task"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to edit!")
            return
        
        item = selected[0]
        task_id = int(self.tree.item(item)['values'][0])
        
        # Find the task
        task_to_edit = None
        for task in self.tasks:
            if task["id"] == task_id:
                task_to_edit = task
                break
        
        if task_to_edit:
            # Create edit dialog
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Task")
            edit_window.geometry("400x300")
            edit_window.configure(bg=self.bg_color)
            edit_window.transient(self.root)
            edit_window.grab_set()
            
            # Center the window
            edit_window.update_idletasks()
            x = self.root.winfo_x() + (self.root.winfo_width() - edit_window.winfo_width()) // 2
            y = self.root.winfo_y() + (self.root.winfo_height() - edit_window.winfo_height()) // 2
            edit_window.geometry(f"+{x}+{y}")
            
            # Task description
            tk.Label(edit_window, 
                    text="Task Description:", 
                    font=("Arial", 11, "bold"),
                    bg=self.bg_color).pack(pady=(20, 5))
            
            task_text_var = tk.StringVar(value=task_to_edit["task"])
            task_entry = tk.Entry(edit_window,
                                textvariable=task_text_var,
                                font=("Arial", 11),
                                width=40)
            task_entry.pack(pady=(0, 15))
            
            # Priority
            tk.Label(edit_window, 
                    text="Priority:", 
                    font=("Arial", 11),
                    bg=self.bg_color).pack()
            
            priority_var = tk.StringVar(value=task_to_edit["priority"])
            priority_combo = ttk.Combobox(edit_window,
                                        textvariable=priority_var,
                                        values=["High", "Medium", "Low"],
                                        state="readonly",
                                        width=15)
            priority_combo.pack(pady=(0, 15))
            
            # Due date
            tk.Label(edit_window, 
                    text="Due Date (YYYY-MM-DD):", 
                    font=("Arial", 11),
                    bg=self.bg_color).pack()
            
            due_date_var = tk.StringVar(value=task_to_edit["due_date"])
            due_date_entry = tk.Entry(edit_window,
                                    textvariable=due_date_var,
                                    font=("Arial", 11),
                                    width=15)
            due_date_entry.pack(pady=(0, 20))
            
            # Save button
            def save_edits():
                task_to_edit["task"] = task_text_var.get().strip()
                task_to_edit["priority"] = priority_var.get()
                due_date = due_date_var.get().strip()
                
                if due_date:
                    try:
                        datetime.strptime(due_date, "%Y-%m-%d")
                        task_to_edit["due_date"] = due_date
                    except ValueError:
                        messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                        return
                else:
                    task_to_edit["due_date"] = ""
                
                self.refresh_task_list()
                self.save_tasks()
                edit_window.destroy()
                messagebox.showinfo("Success", "Task updated successfully!")
            
            save_btn = tk.Button(edit_window,
                               text="💾 Save Changes",
                               command=save_edits,
                               bg=self.accent_color,
                               fg="white",
                               font=("Arial", 11, "bold"),
                               padx=20,
                               pady=8,
                               cursor="hand2")
            save_btn.pack()

    def delete_task(self):
        """Delete selected task"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to delete!")
            return
        
        confirm = messagebox.askyesno("Confirm Delete", 
                                     "Are you sure you want to delete the selected task(s)?")
        if confirm:
            task_ids_to_delete = []
            for item in selected:
                task_id = int(self.tree.item(item)['values'][0])
                task_ids_to_delete.append(task_id)
            
            # Remove tasks
            self.tasks = [task for task in self.tasks if task["id"] not in task_ids_to_delete]
            
            # Reassign IDs
            for i, task in enumerate(self.tasks, 1):
                task["id"] = i
            
            self.refresh_task_list()
            self.update_status_bar()
            self.save_tasks()
            messagebox.showinfo("Success", "Task(s) deleted successfully!")

    def show_statistics(self):
        """Show task statistics"""
        total = len(self.tasks)
        completed = self.count_completed()
        pending = self.count_pending()
        
        # Count by priority
        high = len([t for t in self.tasks if t["priority"] == "High"])
        medium = len([t for t in self.tasks if t["priority"] == "Medium"])
        low = len([t for t in self.tasks if t["priority"] == "Low"])
        
        # Count overdue tasks
        today = datetime.now().date()
        overdue = 0
        for task in self.tasks:
            if task["due_date"] and task["status"] == "Pending":
                try:
                    due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                    if due_date < today:
                        overdue += 1
                except:
                    pass
        
        stats_text = f"""
        📊 Task Statistics
        
        Total Tasks: {total}
        Completed: {completed} ({completed/total*100:.1f}%)
        Pending: {pending} ({pending/total*100:.1f}%)
        
        Priority Breakdown:
        • High: {high} tasks
        • Medium: {medium} tasks
        • Low: {low} tasks
        
        Overdue Tasks: {overdue}
        """
        
        messagebox.showinfo("Task Statistics", stats_text)

    def filter_tasks(self, filter_type):
        """Filter tasks based on criteria"""
        self.filter_status = filter_type
        self.refresh_task_list()

    def refresh_task_list(self):
        """Refresh the task list in Treeview"""
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Apply filter
        filtered_tasks = self.tasks
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        if self.filter_status == "Pending":
            filtered_tasks = [t for t in self.tasks if t["status"] == "Pending"]
        elif self.filter_status == "Completed":
            filtered_tasks = [t for t in self.tasks if t["status"] == "Completed"]
        elif self.filter_status == "High Priority":
            filtered_tasks = [t for t in self.tasks if t["priority"] == "High"]
        elif self.filter_status == "Today":
            filtered_tasks = [t for t in self.tasks if t["due_date"] == today_str]
        
        # Add tasks to treeview
        for task in filtered_tasks:
            status = "✅" if task["status"] == "Completed" else "⏳"
            
            # Color coding for priority
            priority_color = ""
            if task["priority"] == "High":
                priority_color = "🔴"
            elif task["priority"] == "Medium":
                priority_color = "🟡"
            else:
                priority_color = "🟢"
            
            # Check if overdue
            due_date_display = task["due_date"] if task["due_date"] else "No due date"
            if task["due_date"] and task["status"] == "Pending":
                try:
                    due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                    if due_date < datetime.now().date():
                        due_date_display = f"⚠️ {task['due_date']} (OVERDUE)"
                except:
                    pass
            
            values = (task["id"], status, task["task"], 
                     f"{priority_color} {task['priority']}", 
                     due_date_display, task["created"])
            
            item = self.tree.insert("", tk.END, values=values)
            
            # Apply color based on status
            if task["status"] == "Completed":
                self.tree.item(item, tags=("completed",))
            else:
                self.tree.item(item, tags=("pending",))
        
        # Configure tags
        self.tree.tag_configure("completed", background="#d4edda")
        self.tree.tag_configure("pending", background="#fff3cd")

    def count_pending(self):
        """Count pending tasks"""
        return len([t for t in self.tasks if t["status"] == "Pending"])

    def count_completed(self):
        """Count completed tasks"""
        return len([t for t in self.tasks if t["status"] == "Completed"])

    def update_status_bar(self):
        """Update status bar text"""
        self.status_bar.config(
            text=f"Total Tasks: {len(self.tasks)} | "
                 f"Pending: {self.count_pending()} | "
                 f"Completed: {self.count_completed()} | "
                 f"Filter: {self.filter_status}"
        )

    def on_task_double_click(self, event):
        """Handle double-click on task"""
        item = self.tree.identify_row(event.y)
        if item:
            self.mark_complete()

    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.tasks, f, indent=4)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.tasks = json.load(f)
            except:
                self.tasks = []
        else:
            self.tasks = []

    def save_and_exit(self):
        """Save tasks and exit application"""
        self.save_tasks()
        self.root.destroy()

    def on_closing(self):
        """Handle window closing"""
        self.save_tasks()
        self.root.destroy()

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()