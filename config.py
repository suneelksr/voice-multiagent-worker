"""
config.py — Central configuration for the Voice Multi-Agent Worker.

Loads all API keys and settings from environment variables.
Reads from a .env file if present (via python-dotenv).

Import this module anywhere you need a key or setting:

    from config import config
    key = config.GROQ_API_KEY
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from the project root if it exists
_env_path = Path(__file__).parent / ".env"
if _env_path.exists():
    load_dotenv(_env_path)


class Config:
    """All runtime configuration in one place."""

    # ---------- API Keys ----------
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    RETELL_API_KEY: str = os.getenv("RETELL_API_KEY", "")
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    NETLIFY_AUTH_TOKEN: str = os.getenv("NETLIFY_AUTH_TOKEN", "")

    # ---------- LLM Settings ----------
    LLM_MODEL: str = "groq/openai/gpt-oss-20b"
    LLM_TEMPERATURE: float = 0.5
    LLM_MAX_TOKENS: int = 2000

    # ---------- Worker Defaults ----------
    RETELL_AGENT_NAME: str = os.getenv("RETELL_AGENT_NAME", "Multiagent Voice Demo")
    GITHUB_REPO_NAME: str = os.getenv("GITHUB_REPO_NAME", "voice-multiagent-app")
    NETLIFY_SITE_NAME: str = os.getenv("NETLIFY_SITE_NAME", "voice-multiagent-demo")

    # ---------- Agent Behavior ----------
    AGENT_MAX_ITER: int = 15

    @classmethod
    def validate(cls) -> list[str]:
        """
        Return a list of missing required keys.
        Empty list means everything is configured correctly.
        """
        required = {
            "GROQ_API_KEY": cls.GROQ_API_KEY,
            "RETELL_API_KEY": cls.RETELL_API_KEY,
            "GITHUB_TOKEN": cls.GITHUB_TOKEN,
            "NETLIFY_AUTH_TOKEN": cls.NETLIFY_AUTH_TOKEN,
        }
        return [name for name, value in required.items() if not value]

    @classmethod
    def print_status(cls) -> None:
        """Print a human-readable summary of which keys are loaded."""
        keys = {
            "GROQ_API_KEY": cls.GROQ_API_KEY,
            "RETELL_API_KEY": cls.RETELL_API_KEY,
            "GITHUB_TOKEN": cls.GITHUB_TOKEN,
            "NETLIFY_AUTH_TOKEN": cls.NETLIFY_AUTH_TOKEN,
        }
        print("=" * 50)
        print("Configuration Status")
        print("=" * 50)
        for name, value in keys.items():
            status = "✅ loaded" if value else "❌ MISSING"
            masked = f"{value[:8]}..." if value else "(empty)"
            print(f"  {name:<25} {status}  {masked}")
        print("=" * 50)


# Single shared instance — import this everywhere
config = Config()