import os
import shutil
import subprocess

from google.adk.agents import Agent

WORKSPACE_DIR = os.path.join(os.path.dirname(__file__), "workspace")


def _resolve_repo_path(repo_name: str) -> str:
    repo_path = os.path.abspath(os.path.join(WORKSPACE_DIR, repo_name))
    if os.path.commonpath([repo_path, WORKSPACE_DIR]) != WORKSPACE_DIR:
        raise ValueError("repo_name must not escape the workspace directory.")
    return repo_path


def create_git_repo(repo_name: str) -> str:
    """Creates a new folder inside the sandboxed workspace and runs `git init` in it.

    Args:
        repo_name: Name of the folder/repo to create (no slashes or "..").

    Returns:
        A confirmation message, or an error message if the repo already
        exists or git init fails.
    """
    try:
        repo_path = _resolve_repo_path(repo_name)
    except ValueError as e:
        return f"Error: {e}"

    if os.path.exists(repo_path):
        return f"Error: '{repo_name}' already exists at {repo_path}."

    os.makedirs(repo_path)
    result = subprocess.run(
        ["git", "init", repo_path], capture_output=True, text=True
    )
    if result.returncode != 0:
        shutil.rmtree(repo_path, ignore_errors=True)
        return f"Failed to initialize git repo: {result.stderr.strip()}"

    return f"Created git repository '{repo_name}' at {repo_path}."


def delete_git_repo(repo_name: str) -> str:
    """Deletes a git repository folder previously created in the sandboxed workspace.

    Args:
        repo_name: Name of the folder/repo to delete.

    Returns:
        A confirmation message, or an error message if the repo doesn't
        exist or isn't a git repository.
    """
    try:
        repo_path = _resolve_repo_path(repo_name)
    except ValueError as e:
        return f"Error: {e}"

    if not os.path.isdir(repo_path):
        return f"Error: '{repo_name}' does not exist at {repo_path}."
    if not os.path.isdir(os.path.join(repo_path, ".git")):
        return f"Error: '{repo_path}' is not a git repository."

    shutil.rmtree(repo_path)
    return f"Deleted git repository '{repo_name}' at {repo_path}."


root_agent = Agent(
    name="git_tool_agent",
    model="gemini-2.5-flash",
    description=(
        "Agent that can create and delete sandboxed git repositories on request."
    ),
    instruction=(
        "You can create and delete git repositories inside a sandboxed workspace"
        " folder. Use create_git_repo to make a new repo and delete_git_repo to"
        " remove one. Always confirm the repo name with the user before"
        " deleting anything."
    ),
    tools=[create_git_repo, delete_git_repo],
)
