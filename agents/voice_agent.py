"""
agents/voice_agent.py — Voice Infrastructure Engineer agent.

Specializes in Retell AI voice agent provisioning.
"""

from crewai import Agent, LLM
from tools.retell_tool import manage_retell_agent
from config import config


def build_voice_agent() -> Agent:
    """Factory function — returns a configured voice agent."""
    llm = LLM(
        model=config.LLM_MODEL,
        temperature=config.LLM_TEMPERATURE,
        max_tokens=config.LLM_MAX_TOKENS,
    )

    return Agent(
        role="Voice Infrastructure Engineer",
        goal="Configure conversational voice AI agents using Retell AI.",
        backstory=(
            "You are an expert in low-latency voice pipelines and voice API "
            "integrations. You create voice agents that handle real customer "
            "conversations with natural, helpful responses."
        ),
        tools=[manage_retell_agent],
        llm=llm,
        verbose=True,
        max_iter=config.AGENT_MAX_ITER,
    )