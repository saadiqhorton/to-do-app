import json
from time import sleep
from rich import print, console

file = "tasks.json"



def save_file(tasks):
    try:
        with open(file, "w") as f:
            json.dump(tasks, f, indent=4)
    except FileNotFoundError:
        print(f"{file} does not exist, saving as new file.")

def toggle_tasks(tasks):
    view_tasks(tasks)
    try:    
        user_input = input("Which task do you want to mark?: ").casefold()
        if user_input.isdigit():
            index = int(user_input) - 1
            if 0 <= index < len(tasks):
                tasks[index]["completed"] = not tasks[index]["completed"]
                status = "completed" if tasks[index]["completed"] else "not completed"
                print(f"Marked {tasks[index]['title']} as {status}.")
                save_file(tasks)
            else:
                print("Invalid task number")
        else:
            for task in tasks:
                if task["title"].casefold() == user_input:
                    task["completed"] = not task["completed"]
                    status = "completed" if task["completed"] else "not completed"
                    print(f"Marked {task['title']} as {status}.\n")
                    save_file(tasks)
                    break
            else:
                print("Task not found")
                return
    except Exception as e:
        print("ERROR:", e)
    

def go_to_menu(tasks):
    print('\nTo Do List')
    print('-' * 10)
    print("1. add tasks\n2. edit tasks\n3. delete tasks\n4. view tasks\n5. toggle tasks\n6. change order\n7. exit")
    print('-'*10)
    count_complete(tasks)

def add_tasks(tasks):
    task = input('\nEnter task: ').capitalize()
    tasks.append({"title": task, "completed": False})
    with open(file, "w") as filename:
        for task in tasks:
            save_file(tasks)
    print('Task entered successfully')
    sleep(1)
    

def edit_tasks(tasks):
    try:    
        view_tasks(tasks)
        user_input = input("What task would you like to edit? (type 'menu' to go back): ")

        if user_input.lower() == 'menu':
            go_to_menu()
            return
        
        if user_input.isdigit():
            index = int(user_input) - 1
            if 0 <= index <= len(tasks):
                edited_task = input("Enter new name for task: ").title()
                tasks[index]["title"] = edited_task
                print(f"[bold blue]Updated task to:[/bold blue] {edited_task}")
                save_file(tasks)
            else:
                print("Cannot find task")
        else: 
            for task in tasks:
                if task["title"].casefold() == user_input: 
                    edited_task = input("Enter new name for task: ").title()
                    task["title"] = edited_task
                    print(f"[bold blue]Updated task to:[/bold blue] {edited_task}")
                    save_file(tasks)
    except Exception as e:
        print("ERROR:", e)
             
def delete_tasks(tasks):
    view_tasks(tasks)
    while True:    
        
        user_input = input("\nWhat task would you like to remove? (type 'menu' to go back): ")

        if user_input.lower() == 'menu':
            go_to_menu()
            return

        if user_input.isdigit():
            index = int(user_input) - 1
            if 0 <= index < len(tasks):
                confirm = input(f"Are you sure you want to delete '{tasks[index]['title']}?' (y/n): ").lower()
                if confirm == 'y':
                    removed = tasks.pop(index)
                    save_file(tasks)
                    print('Task "{}" removed successfully'.format(removed['title']))
                    return
                elif confirm == 'n':
                    return
                else:
                    print("Enter 'y' or 'n' for confirmation")
            else:
                print('Invalid Number')
        else:
            for task in tasks:
                if task["title"].casefold() == user_input: 
                    confirm = input(f"Are you sure you want to delete '{task['title']}?' (y/n): ").lower()
                    if confirm == 'y':
                        tasks.remove(task)
                        save_file(tasks)
                        print(f'Task "{task["title"]}" removed successfully')
                        return
                    elif confirm == 'n':
                        return
                    else:
                        print("Enter 'y' or 'n' for confirmation")
            else:
                    print('Task not found')
    sleep(1)
    go_to_menu()    

def toggle_fn(task):
    return "[[bold green]x[/bold green]]" if task["completed"] == True else "[ ]"
   
def count_complete(tasks):
    c_count = sum(1 for task in tasks if task["completed"])
    print(f"Completed {c_count}/[bold red]{len(tasks)}[/bold red] tasks\n")

def view_tasks(tasks):
    if tasks == []:
        print('No tasks in To-Do list right now\n')
        sleep(1)
        go_to_menu()
    else:
        for i, task in enumerate(tasks, 1):
            print(f'{i}. {toggle_fn(task)} {task["title"]}')
        sleep(1)
        print()  

def change_order(tasks):
    try:    
        view_tasks(tasks)
        user_input = input("What task would you like to move? (type 'menu' to go back): ")

        if user_input.lower() == 'menu':
            return
        
        if user_input.isdigit():
            index = int(user_input) - 1
            if 0 <= index <= len(tasks):
                position = int(input(f"Where would you like to move '{tasks[index]['title']}'? "))
                if 1 <= position <= len(tasks):
                    task = tasks.pop(index)
                    tasks.insert(position - 1, task)
                    print(f"[bold blue]Moved task to:[/bold blue] #{position}")
                    save_file(tasks)
                
            else:
                print("Cannot find task")
        else:
            found = False
            for i, task in enumerate(tasks):
                if task["title"].casefold() == user_input.casefold():
                    position = int(input(f"Where would you like to move '{task['title']}'? "))
                    if 1 <= position <= len(tasks):
                        moved_task = tasks.pop(i)
                        tasks.insert(position - 1, moved_task)
                        print(f"[bold blue]Moved task to:[/bold blue] #{position}")
                        save_file(tasks)
                    else:
                        print("Invalid position.")
                    found = True
                    break
            if not found:
                print("Task not found.")
    except Exception as e:
        print("ERROR:", e)
    view_tasks(tasks)



