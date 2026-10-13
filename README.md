# Project Management CLI

A command-line tool for managing users, projects, and tasks. Data is saved to `data/project_data.json`. An optional AI feature summarizes a project using a local Ollama model.

## Setup

1. Python 3.10+ is required.
2. Create and activate a virtual environment:
   `python3 -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`

## Running

`python main.py <command> [options]`

## Example commands

    python main.py add-user --name "Alex" --email "alex@example.com"
    python main.py add-user --name "Sam" --email "sam@example.com"
    python main.py list-users
    python main.py add-project --user "Alex" --title "CLI Tool" --description "Build project tracker" --due-date 2026-11-01
    python main.py list-projects --user "Alex"
    python main.py edit-project --project "CLI Tool" --description "Build and document tracker"
    python main.py add-task --project "CLI Tool" --title "Implement add-task command" --assign Alex Sam
    python main.py list-tasks --project "CLI Tool"
    python main.py complete-task --project "CLI Tool" --task "Implement add-task command"
    python main.py summarize-project --project "CLI Tool"

## File structure

- `main.py`: CLI entry point (argparse) and command handlers
- `models/`: `Person`, `User`, `Project`, `Task` classes
- `services/storage_service.py`: JSON save/load
- `services/ai_client.py`: reusable Ollama client
- `utils/formatters.py`: table output with tabulate
- `data/project_data.json`: saved data (created automatically)

## Features

- Create and list users
- Add projects to users (one-to-many)
- Add tasks to projects, assign several users to one task, mark tasks complete
- Edit projects
- Data persists between runs
- AI project summary, risk note, and next step

## External service: Ollama

`summarize-project` sends project and task data to a local model through the `ollama` package.

Setup:
1. Install Ollama from https://ollama.com
2. Pull a model: `ollama pull llama3.2`
3. Make sure Ollama is running, then use `summarize-project`

If Ollama is not running or installed, the CLI prints a clear message instead of crashing.

## Known issues

- Names and titles are matched case-insensitively and must be unique.
- Summary quality depends on the local model.
