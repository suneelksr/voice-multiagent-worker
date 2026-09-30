"""
tools/retell_tool.py — Retell AI voice agent creation tool.

Retell requires a two-step creation process:
  1. Create the LLM (the "brain" — model, prompt, tools).
  2. Create the Agent (the wrapper — voice, language, phone config).

This tool handles both steps in one call.
"""

import requests
from crewai.tools import tool
from config import config

RETELL_API_BASE = "https://api.retellai.com"


def _create_retell_llm(headers: dict, prompt: str) -> tuple[str | None, str | None]:
    """Helper: create the underlying Retell LLM. Returns (llm_id, error)."""
    try:
        response = requests.post(
            f"{RETELL_API_BASE}/create-retell-llm",
            headers=headers,
            json={
                "model": "gpt-4o-mini",
                "general_prompt": prompt,
                "general_tools": [],
            },
            timeout=30,
        )
        if response.status_code not in (200, 201):
            return None, f"Failed ({response.status_code}): {response.text}"
        llm_id = response.json().get("llm_id")
        if not llm_id:
            return None, f"No llm_id returned: {response.text}"
        return llm_id, None
    except requests.Timeout:
        return None, "LLM creation timed out after 30 seconds."
    except Exception as e:
        return None, f"LLM creation connection error: {e}"


def _create_retell_agent(
    headers: dict, agent_name: str, llm_id: str
) -> tuple[dict | None, str | None]:
    """Helper: create the Retell Agent. Returns (agent_data, error)."""
    try:
        response = requests.post(
            f"{RETELL_API_BASE}/create-agent",
            headers=headers,
            json={
                "agent_name": agent_name,
                "voice_id": "11labs-Adrian",
                "response_engine": {
                    "type": "retell-llm",
                    "llm_id": llm_id,
                },
                "language": "en-US",
            },
            timeout=30,
        )
        if response.status_code not in (200, 201):
            return None, f"Failed ({response.status_code}): {response.text}"
        return response.json(), None
    except requests.Timeout:
        return None, "Agent creation timed out after 30 seconds."
    except Exception as e:
        return None, f"Agent creation connection error: {e}"


@tool("Retell Voice Agent Tool")
def manage_retell_agent(agent_name: str) -> str:
    """
    Creates a real Retell AI voice agent (with an underlying LLM) on
    the authenticated user's account.

    Args:
        agent_name: The display name for the agent
                    (e.g., "Customer Support Bot").

    Returns:
        A status string with the agent ID and LLM ID, or an error.
    """
    token = config.RETELL_API_KEY
    if not token:
        return "❌ [Retell] RETELL_API_KEY is not configured."

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # Step 1 — Create the LLM
    prompt = (
        "You are a friendly assistant created by the Voice Multi-Agent Worker. "
        "Keep responses concise and helpful."
    )
    llm_id, error = _create_retell_llm(headers, prompt)
    if error:
        return f"❌ [Retell] LLM creation {error}"

    # Step 2 — Create the Agent
    agent_data, error = _create_retell_agent(headers, agent_name, llm_id)
    if error:
        return f"❌ [Retell] Agent creation {error}"

    agent_id = agent_data.get("agent_id", "unknown")
    return f"⚡ [Retell AI] Voice agent created. Agent ID: {agent_id} | LLM ID: {llm_id}"