# Voice Multi-Agent Worker

A multi-agent AI worker that provisions infrastructure across three platforms — **Retell AI**, **GitHub**, and **Netlify** — from a single natural-language instruction.

Built with **CrewAI** (agent orchestration) and **Groq** (free cloud LLM inference using Llama 3.1 / GPT-OSS 20B).

---

## What It Does

Given a simple task description like:

> "Create a Retell voice agent named 'Demo v1', a GitHub repo named 'demo-repo', and a Netlify site named 'demo-site'."

The worker:

1. Spins up two specialized AI agents
2. Routes the Retell task to a **Voice Infrastructure Engineer** agent
3. Routes the GitHub + Netlify tasks to a **Cloud Delivery Architect** agent
4. Each agent selects the right tool and calls the real REST API
5. Returns verifiable URLs — the actual repo, the live site, the agent ID

Every artifact is real. Nothing is simulated.

---

## Architecture
