import argparse

from models import User, Project, Task
from services.storage_service import StorageService
from services.ai_client import AIClient, AIServiceError
from utils.formatters import print_users, print_projects, print_tasks


def find_user(users, name):
    for user in users:
        if user.name.lower() == name.lower():
            return user
    return None


def find_project(projects, title):
    for project in projects:
        if project.title.lower() == title.lower():
            return project
    return None


def add_user(args, users, projects):
    if find_user(users, args.name):
        print(f"User '{args.name}' already exists.")
        return False
    user = User(args.name, args.email)
    users.append(user)
    print(f"Added user: {user}")
    return True


def list_users(args, users, projects):
    print_users(users)
    return False


def add_project(args, users, projects):
    user = find_user(users, args.user)
    if not user:
        print(f"User '{args.user}' not found.")
        return False
    if find_project(projects, args.title):
        print(f"Project '{args.title}' already exists.")
        return False
    project = Project(args.title, args.description, user.name, args.due_date)
    user.add_project(project)
    projects.append(project)
    print(f"Added project '{project.title}' for {user.name}.")
    return True


def list_projects(args, users, projects):
    if args.user:
        user = find_user(users, args.user)
        if not user:
            print(f"User '{args.user}' not found.")
            return False
        print_projects(user.projects)
    else:
        print_projects(projects)
    return False


def edit_project(args, users, projects):
    project = find_project(projects, args.project)
    if not project:
        print(f"Project '{args.project}' not found.")
        return False
    if args.new_title:
        project.title = args.new_title
    if args.description:
        project.description = args.description
    if args.due_date:
        project.due_date = args.due_date
    print(f"Updated project: {project}")
    return True


def add_task(args, users, projects):
    project = find_project(projects, args.project)
    if not project:
        print(f"Project '{args.project}' not found.")
        return False
    names = []
    for name in args.assign or []:
        user = find_user(users, name)
        if not user:
            print(f"User '{name}' not found.")
            return False
        names.append(user.name)
    task = Task(args.title, assigned_to=names)
    project.add_task(task)
    print(f"Added task: {task}")
    return True


def complete_task(args, users, projects):
    project = find_project(projects, args.project)
    if not project:
        print(f"Project '{args.project}' not found.")
        return False
    task = project.find_task(args.task)
    if not task:
        print(f"Task '{args.task}' not found in '{project.title}'.")
        return False
    task.complete()
    print(f"Completed: {task}")
    return True


def list_tasks(args, users, projects):
    project = find_project(projects, args.project)
    if not project:
        print(f"Project '{args.project}' not found.")
        return False
    print_tasks(project)
    return False


def summarize_project(args, users, projects):
    project = find_project(projects, args.project)
    if not project:
        print(f"Project '{args.project}' not found.")
        return False
    try:
        print(AIClient().summarize_project(project))
    except AIServiceError as error:
        print(f"AI summary unavailable: {error}")
    return False


def build_parser():
    parser = argparse.ArgumentParser(description="Project Management CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add-user", help="Create a user")
    p.add_argument("--name", required=True)
    p.add_argument("--email", required=True)
    p.set_defaults(func=add_user)

    p = sub.add_parser("list-users", help="List all users")
    p.set_defaults(func=list_users)

    p = sub.add_parser("add-project", help="Add a project to a user")
    p.add_argument("--user", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--description", default="")
    p.add_argument("--due-date", default=None)
    p.set_defaults(func=add_project)

    p = sub.add_parser("list-projects", help="List projects (optionally for one user)")
    p.add_argument("--user", default=None)
    p.set_defaults(func=list_projects)

    p = sub.add_parser("edit-project", help="Edit a project")
    p.add_argument("--project", required=True)
    p.add_argument("--new-title", default=None)
    p.add_argument("--description", default=None)
    p.add_argument("--due-date", default=None)
    p.set_defaults(func=edit_project)

    p = sub.add_parser("add-task", help="Add a task to a project")
    p.add_argument("--project", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--assign", nargs="*", help="One or more user names")
    p.set_defaults(func=add_task)

    p = sub.add_parser("complete-task", help="Mark a task complete")
    p.add_argument("--project", required=True)
    p.add_argument("--task", required=True)
    p.set_defaults(func=complete_task)

    p = sub.add_parser("list-tasks", help="List tasks in a project")
    p.add_argument("--project", required=True)
    p.set_defaults(func=list_tasks)

    p = sub.add_parser("summarize-project", help="AI summary of a project")
    p.add_argument("--project", required=True)
    p.set_defaults(func=summarize_project)

    return parser


def main():
    args = build_parser().parse_args()
    storage = StorageService()
    users, projects = storage.load()
    try:
        changed = args.func(args, users, projects)
    except ValueError as error:
        print(f"Error: {error}")
        return
    if changed:
        storage.save(users, projects)


if __name__ == "__main__":
    main()
