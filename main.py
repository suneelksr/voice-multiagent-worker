"""
main.py — Entry point for the Voice Multi-Agent Worker.

Orchestrates two specialized agents to provision infrastructure across
Retell AI, GitHub, and Netlify from a single run.

Usage:
    python main.py
"""

import os
import json
from datetime import datetime

# ==========================================
# 1. PATCH LITELLM BEFORE CREWAI IMPORTS
# ==========================================
# Groq rejects a `cache_breakpoint` field that CrewAI injects into
# system messages. Strip it from every outgoing request.
import litellm

if not getattr(litellm, "_cache_breakpoint_patched", False):
    _real_completion = litellm.completion
    _real_acompletion = litellm.acompletion

    def _strip_bp(kwargs):
        for msg in kwargs.get("messages", []):
            if isinstance(msg, dict):
                msg.pop("cache_breakpoint", None)
                content = msg.get("content")
                if isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict):
                            block.pop("cache_breakpoint", None)
        return kwargs

    def _patched_completion(*args, **kwargs):
        return _real_completion(*args, **_strip_bp(kwargs))

    async def _patched_acompletion(*args, **kwargs):
        return await _real_acompletion(*args, **_strip_bp(kwargs))

    litellm.completion = _patched_completion
    litellm.acompletion = _patched_acompletion
    litellm._cache_breakpoint_patched = True
    print("✅ LiteLLM patched (cache_breakpoint stripped)")


# ==========================================
# 2. IMPORTS
# ==========================================
from crewai import Crew, Process
from config import config
from agents.voice_agent import build_voice_agent
from agents.devops_agent import build_devops_agent
from tasks.tasks import build_voice_task, build_deploy_task


# ==========================================
# 3. MAIN
# ==========================================
def main():
    # --- Validate configuration ---
    missing = config.validate()
    if missing:
        print("❌ Missing required environment variables:")
        for name in missing:
            print(f"   - {name}")
        print("\nCopy .env.example to .env and fill in real values.")
        return

    config.print_status()

    # --- Build agents ---
    print("\n🔧 Building agents...")
    voice_agent = build_voice_agent()
    devops_agent = build_devops_agent()

    # --- Build tasks ---
    print("📋 Building tasks...")
    voice_task = build_voice_task(voice_agent)
    deploy_task = build_deploy_task(devops_agent)

    # --- Assemble the crew ---
    crew = Crew(
        agents=[voice_agent, devops_agent],
        tasks=[voice_task, deploy_task],
        process=Process.sequential,
        verbose=True,
    )

    # --- Run ---
    print("\n🚀 Starting Multi-Agent Worker...\n")
    result = crew.kickoff()

    print("\n=== WORKER FINISHED ===")
    print(result)

    # --- Log to disk ---
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"run_{timestamp}.json")

    log_payload = {
        "timestamp": datetime.now().isoformat(),
        "result": str(result),
        "agent_count": len(crew.agents),
        "task_count": len(crew.tasks),
        "llm_model": config.LLM_MODEL,
    }
    with open(log_file, "w") as f:
        json.dump(log_payload, f, indent=2)

    print(f"\n📁 Log saved: {log_file}")


if __name__ == "__main__":
    main()