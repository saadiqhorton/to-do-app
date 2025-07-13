import tkinter as tk
from tkinter import ttk
import json
import functions

dark_bg = "#1d1e25"
light_text = "#f5f5f5"
accent = "#4e9af1"  
font_main = ("Segoe UI", 11)
font_title = ("Segoe UI", 16, "bold")

category_colors = {
    "work": "#e8e22c",
    "personal": "#2f82ee",
    "study": "#51f43b",
    "health": "#d82727",
    "productivity": "#b43dfa",
    "default": "#1d1e25"
}

category_options = [cat.capitalize() for cat in category_colors]


def on_enter(e, button, color):
    button['background'] = color

def on_leave(e, button, original_color):
    button["background"] = original_color

file = "tasks.json"

def load_tasks():
    try:
        with open(file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open(file, "w") as f:
        json.dump(tasks, f, indent=4)

root = tk.Tk()
root.configure(bg=dark_bg)
root.title("To-Do List")
root.geometry("500x600")

title = tk.Label(root, text="To-Do List", font=font_title, fg=light_text, bg=dark_bg)
title.pack(pady=(10, 5))

input_frame = tk.Frame(root, bg=dark_bg)
input_frame.pack(pady=10)

frame = tk.Frame(root)
frame.pack(fill="both", expand=True)


entry = tk.Entry(input_frame, font=font_main, bg="#333", fg=light_text, insertbackground=light_text, width=25)
entry.grid(row=0, column=0, padx=5)



category_var = tk.StringVar()
category_combo = ttk.Combobox(input_frame, textvariable=category_var,
                              values=category_options,
                              font=font_main,
                              state="readonly",
                              width=25)
color_preview = tk.Canvas(input_frame, width=20, height=20, bg=dark_bg, highlightthickness=0)
color_preview.grid(row=1, column=2, padx=5, pady=2)

# Draw a circle (oval) inside the canvas; keep a reference to the shape's id
circle_id = color_preview.create_oval(2, 2, 18, 18, fill=category_colors["default"], outline="")

def update_color_preview(event=None):
    cat = category_var.get().strip().lower()
    color = category_colors.get(cat, category_colors["default"])
    color_preview.itemconfig(circle_id, fill=color)

# Bind to combobox selection changes
category_combo.bind("<<ComboboxSelected>>", update_color_preview)
update_color_preview()
category_combo.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")
category_combo.set("Select Category")  # Placeholder text


add_btn = tk.Button(input_frame, text="Add", command=lambda: add_func(tasks),
                    font=font_main, bg=accent, fg="white", relief="flat", width=6)
add_btn.grid(row=0, column=1, padx=5)
add_btn.bind("<Enter>", lambda e: on_enter(e, add_btn, "#5aaefc"))
add_btn.bind("<Leave>", lambda e: on_leave(e, add_btn, accent))

del_btn = tk.Button(input_frame, text="Delete", command=lambda: delete_func(tasks),
                    font=font_main, bg="#aa3333", fg="white", relief="flat", width=6)
del_btn.grid(row=0, column=2, padx=5)
del_btn.bind("<Enter>", lambda e: on_enter(e, del_btn, "#cc4444"))
del_btn.bind("<Leave>", lambda e: on_leave(e, del_btn, "#aa3333"))

tasks = load_tasks()


edit_mode = False
edit_index = None

edit_entry = tk.Entry(input_frame, font=font_main, bg="#333", fg=light_text, insertbackground=light_text, width=25)
edit_entry.grid(row=2, column=0, columnspan=3, pady=5)
edit_entry.grid_remove()  # Hide it initially
edit_btn = tk.Button(input_frame, text="Edit", command=lambda: enter_edit_mode(entry.get().strip()),
                     font=font_main, bg="#ffaa33", fg="white", relief="flat", width=6)
edit_btn.grid(row=0, column=3, padx=5)

def enter_edit_mode(original_title):
    global edit_mode, edit_index
    for i, task in enumerate(tasks):
        if task["title"].lower() == original_title.lower():
            edit_mode = True
            edit_index = i
            edit_entry.delete(0, tk.END)
            edit_entry.insert(0, task["title"])
            edit_entry.grid()  # Show the field
            return
    print("Task to edit not found.")



def toggle_completion(index, var):
    tasks[index]["completed"] = var.get()
    save_tasks(tasks)
    show_tasks()

def show_tasks():
    
    for widget in frame.winfo_children():
        widget.destroy()

    for i, task in enumerate(tasks):
        task_title = task["title"]
        completed = task.get("completed", False)
        category = task.get("category", "default")
        color = category_colors.get(category.lower(), category_colors["default"])

        task_frame = tk.Frame(frame, bg=color, padx=5, pady=5)
        task_frame.pack(fill="x", padx=10, pady=4)

        

        # Left frame: label + checkbox side by side
        left_frame = tk.Frame(task_frame, bg=color)
        left_frame.pack(side="left")

        label = tk.Label(left_frame, text=f"{i + 1}. {task_title}",
                        font=font_main, fg="white", bg=color, anchor="w")
        label.pack(side="left")

        var = tk.BooleanVar(value=completed)
        checkbox = tk.Checkbutton(left_frame, variable=var, bg=color,
                                command=lambda i=i, v=var: toggle_completion(i, v))
        checkbox.pack(side="left", padx=(5, 0))  # small gap after label
        def move_task_up(index):
            if index > 0:
                tasks[index], tasks[index-1] = tasks[index-1], tasks[index]
                save_tasks(tasks)
                show_tasks()

        def move_task_down(index):  
            if index < len(tasks) - 1:
                tasks[index], tasks[index+1] = tasks[index+1], tasks[index]
                save_tasks(tasks)
                show_tasks()
        # Spacer frame to push buttons to the right
        spacer = tk.Frame(task_frame, bg=color)
        spacer.pack(side="left", expand=True, fill="x")

        # Right frame: Up and Down buttons side by side
        right_frame = tk.Frame(task_frame, bg=color)
        right_frame.pack(side="right")

        up_btn = tk.Button(right_frame, text="▲", width=2, command=lambda i=i: move_task_up(i))
        down_btn = tk.Button(right_frame, text="▼", width=2, command=lambda i=i: move_task_down(i))
        up_btn.pack(side="left", padx=(0, 2))
        down_btn.pack(side="left")
    completed = sum(1 for task in tasks if task["completed"])
    counter = tk.Label(frame, text=f"Completed {completed}/{len(tasks)} tasks",
                       font=("Segoe UI", 12, "italic"),
                       fg="white", bg=dark_bg)
    counter.pack(pady=(10, 0))

    

def add_func(tasks):
    global edit_mode, edit_index
    task_title = entry.get().strip()
    task_category = category_var.get().strip().lower()

    if task_category == "select category" or task_category == "":
        task_category = "default"

    if edit_mode and edit_index is not None:
        new_title = edit_entry.get().strip()
        if new_title:
            tasks[edit_index]["title"] = new_title
            tasks[edit_index]["category"] = task_category
            edit_mode = False
            edit_index = None
            edit_entry.grid_remove()
            save_tasks(tasks)
            show_tasks()
            entry.delete(0, tk.END)
            category_combo.set("Select Category")
        return

    # Standard add/update logic
    if not task_title:
        return

    for task in tasks:
        if task["title"].lower() == task_title.lower():
            task["category"] = task_category
            save_tasks(tasks)
            show_tasks()
            entry.delete(0, tk.END)
            category_combo.set("Select Category")
            return

    # New task
    tasks.append({
        "title": task_title,
        "category": task_category,
        "completed": False
    })
    save_tasks(tasks)
    show_tasks()
    entry.delete(0, tk.END)
    category_combo.set("Select Category")



def delete_func(tasks):
    task_title = entry.get().strip()
    for task in tasks:
        if task["title"].lower() == task_title.lower():
            tasks.remove(task)
            save_tasks(tasks)
            show_tasks()
            entry.delete(0, tk.END)
            return
        
    if task_title.isdigit():
        index = int(task_title) - 1
            
        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            save_tasks(tasks)
            show_tasks()
            entry.delete(0, tk.END)
            return
    else:
        print("Task not found.")
# def delete_button():
#     delete = tk.Button(text="Delete Task", command=lambda: delete_func(tasks))       
#     delete.pack(pady=5)





show_tasks()
root.mainloop()


