from .person import Person


class User(Person):
    """A user who owns projects. Inherits name/email from Person."""

    _next_id = 1  # class attribute used as an ID counter

    def __init__(self, name, email, user_id=None):
        super().__init__(name, email)
        if user_id is None:
            user_id = User._next_id
        User._next_id = max(User._next_id, user_id + 1)
        self.id = user_id
        self.projects = []  # one-to-many: one user -> many projects

    def add_project(self, project):
        """Link a project to this user."""
        self.projects.append(project)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["email"], data["id"])

    def __str__(self):
        return f"{self.name} <{self.email}>"

    def __repr__(self):
        return f"User(id={self.id}, name={self.name!r})"
