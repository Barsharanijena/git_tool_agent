# Git Tool Agent

A [Google ADK](https://google.github.io/adk-docs/) agent that creates and deletes sandboxed git repositories on request.

## What it does

- `create_git_repo(repo_name)` — creates a new folder inside a sandboxed `workspace/` directory and runs `git init` in it
- `delete_git_repo(repo_name)` — deletes a previously created sandboxed repo folder

All operations are restricted to the `workspace/` directory (path traversal via `..` or absolute paths is rejected), so the agent can't touch anything outside its sandbox.

## Tech stack

- `google-adk` (`Agent`)
- Model: `gemini-2.5-flash`

## Setup

1. Copy `.env.example` to `.env` (not included in this repo) and set your Google Cloud / Vertex AI credentials.
2. Run with the ADK CLI: `adk run git_tool_agent`

## Note

This is a learning/demo project built while exploring the Google Agent Development Kit.
