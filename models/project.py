from .task import Task


class Project:
    """A project owned by one user. It holds many tasks."""

    _next_id = 1

    def __init__(self, title, description, owner_name, due_date=None, project_id=None):
        self.title = title
        self.description = description
        self.owner_name = owner_name
        self.due_date = due_date
        if project_id is None:
            project_id = Project._next_id
        Project._next_id = max(Project._next_id, project_id + 1)
        self.id = project_id
        self.tasks = []  # one-to-many: one project -> many tasks

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not value.strip():
            raise ValueError("Project title cannot be empty.")
        self._title = value.strip()

    def add_task(self, task):
        self.tasks.append(task)

    def find_task(self, title):
        for task in self.tasks:
            if task.title.lower() == title.lower():
                return task
        return None

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "owner_name": self.owner_name,
            "due_date": self.due_date,
            "tasks": [t.to_dict() for t in self.tasks],
        }

    @classmethod
    def from_dict(cls, data):
        project = cls(
            data["title"],
            data.get("description", ""),
            data["owner_name"],
            data.get("due_date"),
            data["id"],
        )
        for task_data in data.get("tasks", []):
            project.add_task(Task.from_dict(task_data))
        return project

    def __str__(self):
        done = sum(1 for t in self.tasks if t.status == "complete")
        return f"{self.title} ({done}/{len(self.tasks)} tasks done)"

    def __repr__(self):
        return f"Project(id={self.id}, title={self.title!r})"
