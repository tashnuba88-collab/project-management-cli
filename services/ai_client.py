class AIServiceError(Exception):
    """Raised when the AI service cannot return a result."""


class AIClient:
    """Reusable client that sends project data to a local Ollama model."""

    def __init__(self, model="llama3.2"):
        self.model = model

    def _build_prompt(self, project):
        lines = [
            f"Project: {project.title}",
            f"Description: {project.description}",
            f"Due date: {project.due_date or 'not set'}",
            "Tasks:",
        ]
        for task in project.tasks:
            lines.append(f"- {task}")
        data = "\n".join(lines)
        return (
            "Write a short project summary (2-3 sentences), one risk note, "
            "and one suggested next step based on this data:\n\n" + data
        )

    def summarize_project(self, project):
        try:
            import ollama
        except ImportError:
            raise AIServiceError("The 'ollama' package is not installed. Run: pip install -r requirements.txt")

        try:
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": self._build_prompt(project)}],
            )
            return response["message"]["content"]
        except Exception as error:
            raise AIServiceError(
                f"Could not reach Ollama ({error}). Make sure Ollama is running "
                f"and the model is installed with: ollama pull {self.model}"
            )
