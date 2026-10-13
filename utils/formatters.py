from tabulate import tabulate


def print_users(users):
    if not users:
        print("No users yet.")
        return
    rows = [[u.id, u.name, u.email, len(u.projects)] for u in users]
    print(tabulate(rows, headers=["ID", "Name", "Email", "Projects"], tablefmt="grid"))


def print_projects(projects):
    if not projects:
        print("No projects found.")
        return
    rows = [[p.id, p.title, p.description, p.due_date or "-", str(p)] for p in projects]
    print(tabulate(rows, headers=["ID", "Title", "Description", "Due", "Progress"], tablefmt="grid"))


def print_tasks(project):
    if not project.tasks:
        print(f"No tasks in '{project.title}'.")
        return
    rows = [
        [t.id, t.title, t.status, ", ".join(t.assigned_to) or "-"]
        for t in project.tasks
    ]
    print(tabulate(rows, headers=["ID", "Task", "Status", "Assigned to"], tablefmt="grid"))
