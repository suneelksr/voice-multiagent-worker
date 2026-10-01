# Voice Multi-Agent Worker

A multi-agent AI worker that provisions infrastructure across three platforms: **Retell AI**, **GitHub**, and **Netlify**, from a single natural-language instruction.

Built with **CrewAI** (agent orchestration) and **Groq** (free cloud LLM inference using GPT-OSS 20B).

## Table of Contents

1. What It Does
2. Architecture
3. Stack
4. Project Structure
5. Setup
6. Usage
7. Example Output
8. Design Notes
9. Known Limitations
10. Roadmap
11. License

## What It Does

Given a simple task description like:

> "Create a Retell voice agent named 'Demo v1', a GitHub repo named 'demo-repo', and a Netlify site named 'demo-site'."

The worker:

1. Spins up two specialized AI agents
2. Routes the Retell task to a **Voice Infrastructure Engineer** agent
3. Routes the GitHub and Netlify tasks to a **Cloud Delivery Architect** agent
4. Each agent selects the right tool and calls the real REST API
5. Returns verifiable URLs: the actual repo, the live site, the agent ID

Every artifact is real. Nothing is simulated.

## Architecture
Natural-Language Task
|
v
CrewAI Orchestrator
|
+----+----+
v v
Voice Cloud
Agent Delivery
Agent
| |
v v
Retell GitHub +
API Netlify

## Stack

| Component | Purpose |
|---|---|
| **CrewAI** | Multi-agent orchestration framework |
| **Groq Cloud** | Free LLM inference (GPT-OSS 20B) |
| **LiteLLM** | Provider bridge for CrewAI to Groq |
| **Retell AI** | Voice agent provisioning |
| **GitHub REST API** | Repository creation |
| **Netlify REST API** | Site deployment |
| **python-dotenv** | Environment variable loading |
| **requests** | HTTP client |

## Project Structure
voice-multiagent-worker/
|
|-- main.py Entry point
|-- config.py Central configuration loader
|-- requirements.txt Python dependencies
|-- .env.example Template for API keys
|-- .gitignore Excludes .env, logs, pycache
|-- README.md This file
|
|-- agents/
| |-- init.py
| |-- voice_agent.py Voice Infrastructure Engineer
| +-- devops_agent.py Cloud Delivery Architect
|
|-- tasks/
| |-- init.py
| +-- tasks.py Task definitions
|
+-- tools/
|-- init.py
|-- retell_tool.py Retell API wrapper
|-- github_tool.py GitHub API wrapper
+-- netlify_tool.py Netlify API wrapper

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/suneelksr/voice-multiagent-worker.git
cd voice-multiagent-worker

```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API keys

```bash
cp .env.example .env
```

Then edit `.env` and fill in your real keys:

| Variable | Where to get it |
|---|---|
| `GROQ_API_KEY` | https://console.groq.com/keys |
| `RETELL_API_KEY` | Retell dashboard, API Keys (non-webhook) |
| `GITHUB_TOKEN` | https://github.com/settings/tokens (repo scope) |
| `NETLIFY_AUTH_TOKEN` | https://app.netlify.com/user/applications |

### 4. Verify your environment

Before the first run, confirm all keys are loaded:

```bash
python -c "from config import config; config.print_status()"
```

You should see all four keys marked as loaded.

## Usage

```bash
python main.py
```

The worker will:

1. Load your API keys from `.env`
2. Apply the LiteLLM patch for Groq compatibility
3. Build the two specialized agents
4. Execute the tasks sequentially
5. Return three real URLs (Retell agent ID, GitHub repo, Netlify site)
6. Save an execution log to `logs/run_YYYYMMDD_HHMMSS.json`

## Example Output

```
==================================================
Configuration Status
==================================================
  GROQ_API_KEY              loaded  gsk_xxxx...
  RETELL_API_KEY            loaded  key_xxxx...
  GITHUB_TOKEN              loaded  ghp_xxxx...
  NETLIFY_AUTH_TOKEN        loaded  nft_xxxx...
==================================================

Building agents...
Building tasks...

Starting Multi-Agent Worker...

=== WORKER FINISHED ===
[Retell AI] Voice agent created. Agent ID: agent_xxxxx
[GitHub] Repository created: https://github.com/user/repo-name
[Netlify] Site created: https://site-name.netlify.app

Log saved: logs/run_20261001_143022.json
```

---

## How It Works Internally

The worker uses a **two-agent sequential crew**:

**Agent 1 - Voice Infrastructure Engineer**
Receives the Retell task. Creates an LLM in Retell, then creates the voice agent using that LLM ID. Returns the agent ID to the log.

**Agent 2 - Cloud Delivery Architect**
Receives the GitHub and Netlify tasks. Calls the GitHub REST API to create a repository, then calls the Netlify REST API to deploy a site. Returns both URLs.

**Groq Compatibility Patch**
CrewAI injects a `cache_breakpoint` field into system messages that Groq rejects. The `main.py` file applies an idempotent patch to LiteLLM that strips this field before every request. This is why the worker runs cleanly on Groq's free tier.

## Design Notes

- **BYOK (Bring Your Own Key):** All API keys belong to the user. No third-party billing. No hidden costs.
- **Free LLM:** Uses Groq's free tier, no OpenAI/Anthropic spend.
- **Idempotent:** Safe to re-run; the LiteLLM patch applies once per session.
- **Logs preserved:** Every run writes a JSON log for audit trails.

## Known Limitations

- Retell's free trial credits are consumed by each agent creation (roughly $0.07 to $0.31 per minute)
- Netlify site names must be globally unique, collisions return HTTP 422
- Groq's free tier has a rate limit (roughly 8,000 tokens per minute)

## Troubleshooting

**Error: "Invalid API Key" from Groq**
Your `GROQ_API_KEY` in `.env` is wrong or a placeholder. Verify it starts with `gsk_` and is 50+ characters.

**Error: "401" from any service**
One of your API keys has expired or is missing. Check the `config.print_status()` output.

**Error: "422 name already exists"**
The repo or site name is already taken. Change `GITHUB_REPO_NAME` or `NETLIFY_SITE_NAME` in `.env`.

**Error: "cache_breakpoint is unsupported"**
The LiteLLM patch did not apply. Restart Python and re-run. The patch is idempotent, so re-running is always safe.

## Roadmap

- [ ] Add OAuth-based onboarding (no manual key copying)
- [ ] Support additional voice providers (ElevenLabs, PlayHT)
- [ ] Add optional database provisioning (Supabase, Postgres)
- [ ] Web UI for non-technical clients

## License

MIT. Free to use, modify, and distribute.