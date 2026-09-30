"""
agents/devops_agent.py — Cloud Delivery Architect agent.

Specializes in GitHub repository provisioning and Netlify deployments.
"""

from crewai import Agent, LLM
from tools.github_tool import setup_github_repository
from tools.netlify_tool import deploy_to_netlify
from config import config


def build_devops_agent() -> Agent:
    """Factory function — returns a configured DevOps agent."""
    llm = LLM(
        model=config.LLM_MODEL,
        temperature=config.LLM_TEMPERATURE,
        max_tokens=config.LLM_MAX_TOKENS,
    )

    return Agent(
        role="Cloud Delivery Architect",
        goal="Manage GitHub repositories and deploy sites to Netlify.",
        backstory=(
            "You automate code hosting and static site deployments. You know "
            "how to create repositories, handle name collisions, and deploy "
            "frontends with zero friction."
        ),
        tools=[setup_github_repository, deploy_to_netlify],
        llm=llm,
        verbose=True,
        max_iter=config.AGENT_MAX_ITER,
    )