VALID_STATUSES = ("pending", "complete")


class Task:
    """A task inside a project. Many users can be assigned to one task."""

    _next_id = 1

    def __init__(self, title, status="pending", assigned_to=None, task_id=None):
        self.title = title
        self.status = status
        self.assigned_to = assigned_to or []  # list of user names (many-to-many)
        if task_id is None:
            task_id = Task._next_id
        Task._next_id = max(Task._next_id, task_id + 1)
        self.id = task_id

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in VALID_STATUSES:
            raise ValueError(f"Status must be one of {VALID_STATUSES}.")
        self._status = value

    def complete(self):
        self.status = "complete"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "assigned_to": self.assigned_to,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["title"],
            data.get("status", "pending"),
            data.get("assigned_to", []),
            data["id"],
        )

    def __str__(self):
        who = ", ".join(self.assigned_to) if self.assigned_to else "unassigned"
        return f"[{self.status}] {self.title} ({who})"

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title!r})"
