import json
import os

from models import User, Project


class StorageService:
    """Saves and loads users and projects (with tasks) as JSON."""

    def __init__(self, path="data/project_data.json"):
        self.path = path

    def load(self):
        """Return (users, projects). Starts empty if the file is missing or broken."""
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
            users = [User.from_dict(u) for u in data.get("users", [])]
            projects = [Project.from_dict(p) for p in data.get("projects", [])]
        except FileNotFoundError:
            return [], []
        except (json.JSONDecodeError, KeyError, ValueError) as error:
            print(f"Warning: data file is damaged ({error}). Starting empty.")
            return [], []

        # Rebuild the user -> projects relationship
        for project in projects:
            for user in users:
                if user.name.lower() == project.owner_name.lower():
                    user.add_project(project)
        return users, projects

    def save(self, users, projects):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        data = {
            "users": [u.to_dict() for u in users],
            "projects": [p.to_dict() for p in projects],
        }
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)
