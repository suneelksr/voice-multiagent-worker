"""
tools/github_tool.py — GitHub repository creation tool.

Wraps the GitHub REST API `POST /user/repos` endpoint in a
CrewAI-compatible tool that agents can call.
"""

import requests
from crewai.tools import tool
from config import config


@tool("GitHub Repo Tool")
def setup_github_repository(repo_name: str, description: str = "") -> str:
    """
    Creates a real GitHub repository on the authenticated user's account.

    Args:
        repo_name: The name for the new repository (e.g., "my-project").
        description: Optional short description for the repo.

    Returns:
        A status string indicating success (with repo URL) or failure.
    """
    token = config.GITHUB_TOKEN
    if not token:
        return "❌ [GitHub] GITHUB_TOKEN is not configured."

    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    payload = {
        "name": repo_name,
        "description": description or "Created by Voice Multi-Agent Worker",
        "private": False,
        "auto_init": True,
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code == 201:
            data = response.json()
            return f"🐙 [GitHub] Repository created: {data['html_url']}"
        if response.status_code == 422:
            # Most likely the repo already exists
            return (
                f"❌ [GitHub] Failed (422 — likely name collision): "
                f"{response.json().get('errors', response.text)}"
            )
        return f"❌ [GitHub] Failed ({response.status_code}): {response.text}"
    except requests.Timeout:
        return "❌ [GitHub] Request timed out after 30 seconds."
    except Exception as e:
        return f"❌ [GitHub] Connection error: {e}"