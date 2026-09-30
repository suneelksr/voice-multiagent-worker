"""
tasks/tasks.py — Task definitions for the Voice Multi-Agent Worker.

Each task is a clear instruction for one agent. Tasks run sequentially:
  1. Voice task runs first (Retell agent creation).
  2. Deploy task runs second (GitHub + Netlify provisioning).
"""

from crewai import Task
from config import config


def build_voice_task(agent) -> Task:
    """Task for the Voice Infrastructure Engineer agent."""
    return Task(
        description=(
            f"Create a real Retell AI voice agent named "
            f"'{config.RETELL_AGENT_NAME}'. Return the agent ID and LLM ID."
        ),
        expected_output="Confirmation message containing the Retell agent ID.",
        agent=agent,
    )


def build_deploy_task(agent) -> Task:
    """Task for the Cloud Delivery Architect agent."""
    return Task(
        description=(
            f"1. Create a GitHub repository named '{config.GITHUB_REPO_NAME}'.\n"
            f"2. Create a Netlify site named '{config.NETLIFY_SITE_NAME}'.\n"
            f"Return both the GitHub repo URL and the Netlify live site URL."
        ),
        expected_output="GitHub repository URL and Netlify live site URL.",
        agent=agent,
    )