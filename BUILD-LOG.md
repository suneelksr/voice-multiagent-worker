# Voice Multi-Agent Worker — Build Log

**Project:** Multi-agent AI worker that provisions Retell voice agents, GitHub repositories, and Netlify sites from a single natural-language instruction.

**Status:** Shipped — public GitHub repo, live artifacts, running locally on Windows.

**Build period:** Multi-session development

**Final repo:** https://github.com/suneelksr/voice-multiagent-worker


## Table of Contents

1. Project Goal
2. Constraints & Decisions
3. Architecture
4. Build Timeline — Session by Session
5. Obstacles & Fixes
6. Final File Structure
7. Tech Stack
8. Proof of Work
9. What Was Learned
10. Next Steps



## 1. Project Goal

Build a free multi-agent worker that automates infrastructure provisioning across three services:

- Retell AI — voice agent creation
- GitHub — repository creation
- Netlify — site deployment

Requirements:

- Completely free (no LLM API costs)
- Runs on a low-spec laptop (Intel Core i3, 8GB RAM)
- Client-facing design: each client uses their own accounts (BYOK model)
- Production-shaped codebase, not a notebook experiment


## 2. Constraints & Decisions

| Constraint | Impact | Decision |
|---|---|---|
| Old laptop (i3, 8GB RAM) | Can't run local LLMs | Move processing to cloud |
| Zero budget | Can't pay for LLM APIs | Use Groq free tier |
| Colab runtime limits | Can't run 24/7 from Colab | Package as local Python project |
| Client billing concerns | Don't want to hold client costs | Adopt BYOK (Bring Your Own Key) model |
| Time efficiency | Can't waste weeks on frameworks | Use CrewAI, not custom orchestration |



## 3. Architecture
┌──────────────────────┐
│ Natural-Language │
│ Task Description │
└──────────┬───────────┘
│
▼
┌──────────────────────┐
│ CrewAI Orchestrator │
│ (routes tasks) │
└──────────┬───────────┘
│
┌──────┴──────┐
▼ ▼
┌─────────┐ ┌──────────────┐
│ Voice │ │ Cloud │
│ Agent │ │ Delivery │
│ │ │ Agent │
└────┬────┘ └──────┬───────┘
│ │
▼ ▼
┌─────────┐ ┌──────────────┐
│ Retell │ │ GitHub + │
│ API │ │ Netlify API │
└─────────┘ └──────────────┘


## 4. Build Timeline — Session by Session

### Session 1 — Initial Exploration

- Original goal: build a desktop agent worker from scratch
- Considered three approaches: hand-coded Python, OpenWorker (Andrew Ng framework), SAP Desktop Agent
- Ruled out: OpenWorker (heavy on laptop), SAP (enterprise-only)
- Chose: CrewAI + free LLM

### Session 2 — Hardware Reality Check

- Discovered laptop specs made local Ollama unviable (would freeze)
- Pivoted to cloud LLMs via Groq free tier
- Groq offers fast inference for Llama 3.1 / GPT-OSS 20B at no cost

### Session 3 — Colab Prototype

- Built first working multi-agent pipeline in Google Colab
- Simulated tools to test flow without API keys
- Colab proved viability; but had limits (ephemeral sessions, no scheduled runs)

### Session 4 — Solving Provider Incompatibilities

- Discovered CrewAI requires LiteLLM package for Groq
- Encountered cache_breakpoint error — CrewAI injects unsupported field into Groq requests
- Wrote an idempotent sanitizer to strip the field before sending

### Session 5 — Real Integrations

- Activated real APIs one at a time:
  - Retell: two-step agent+LLM creation
  - GitHub: repo creation via REST
  - Netlify: site deployment via REST
- All three worked from Colab with real credentials

### Session 6 — Persistence & Logging

- Added execution log writing (JSON) for audit trail
- Fought Google Drive OAuth (Windows hijacked URLs to desktop app)
- Pivoted to direct file download — simpler, more reliable

### Session 7 — Packaging as a Python Project

- Restructured single-cell Colab code into a proper multi-file project:
  - config.py — central env var loading
  - tools/ — one file per integration
  - agents/ — one file per agent
  - tasks/ — task definitions
  - main.py — entry point orchestrator
- Added .env.example, .gitignore, requirements.txt, README.md

### Session 8 — Local Run & Debugging

- Ran python main.py locally for the first time
- Initial failure: .env still had placeholder values
- Fixed: replaced with real keys
- Successful run: Retell agent created, GitHub repo created, Netlify site deployed
- Log written to logs/

### Session 9 — GitHub Deployment

- Pushed to public repo: voice-multiagent-worker
- 15 files, 624 insertions
- Verified .env is gitignored (keys never committed)

### Session 10 — Portfolio Evidence

- Created portfolio-evidence folder:
  - runs/ — two execution logs (Colab + local)
  - screenshots/ — 6 numbered evidence images
  - demos/ — placeholder for future recordings



## 5. Obstacles & Fixes

| Obstacle | Cause | Solution |
|---|---|---|
| Laptop too weak for local LLM | 8GB RAM, no GPU | Moved to cloud LLM (Groq) |
| Groq rejected for cache_breakpoint | CrewAI injects unsupported field | Idempotent sanitizer patch in main.py |
| Recursive monkey patch | Patch stacked on itself across cell runs | _cache_breakpoint_patched flag |
| Model llama-3.1-8b-instant retired | Groq deprecation (mid-2026) | Switched to groq/openai/gpt-oss-20b |
| Retell "Invalid response engine" | Missing LLM (agent requires LLM first) | Two-step creation: LLM then Agent |
| Recursion from stacked async patches | Duplicate sanitize cells | Restart runtime and delete old cells |
| Google Drive OAuth hijacked by desktop app | Windows URL handler | Skipped Drive, used file download |
| Files landing in nested folders | VS Code New File context bug | Switched to New-Item from terminal |
| main.py created empty | New-Item doesn't paste content | Open with code, paste, save |



## 6. Final File Structure
voice-multiagent-worker/
├── .env.example # Template for env vars
├── .gitignore # Excludes .env, logs, pycache
├── README.md # Project description
├── config.py # Central config loader
├── main.py # Entry point + LiteLLM patch
├── requirements.txt # Python dependencies
├── agents/
│ ├── init.py
│ ├── devops_agent.py # Cloud Delivery Architect
│ └── voice_agent.py # Voice Infrastructure Engineer
├── tasks/
│ ├── init.py
│ └── tasks.py # Task definitions
└── tools/
├── init.py
├── github_tool.py # GitHub REST API wrapper
├── netlify_tool.py # Netlify REST API wrapper
└── retell_tool.py # Retell REST API wrapper


## 7. Tech Stack

| Component | Purpose |
|---|---|
| CrewAI | Multi-agent orchestration framework |
| Groq Cloud | Free LLM inference (GPT-OSS 20B) |
| LiteLLM | Provider bridge for CrewAI → Groq |
| Retell AI | Voice agent provisioning |
| GitHub REST API | Repository creation |
| Netlify REST API | Site deployment |
| python-dotenv | .env file loading |
| requests | HTTP client for API calls |
| VS Code + Git Bash | Development environment |
| Windows 11 | Host OS |



## 8. Proof of Work

| Artifact | Location |
|---|---|
| GitHub repo | https://github.com/suneelksr/voice-multiagent-worker |
| Live Netlify site | https://voice-multiagent-demo-local.netlify.app |
| Retell agent ID | agent_xxxxx (example) |
| Execution logs | portfolio-evidence/runs/ |
| Screenshots | portfolio-evidence/screenshots/ |


## 9. What Was Learned

### Technical

- CrewAI requires LiteLLM for non-native providers (Groq, Anthropic, etc.)
- Groq rejects the cache_breakpoint field that CrewAI injects — needs a sanitizer patch
- Retell's API is two-step: create LLM, then create Agent
- Idempotent patches (with guard flags) prevent recursion in long-lived kernels
- Windows URL handlers can hijack OAuth flows intended for browsers

### Architectural

- BYOK (Bring Your Own Key) model eliminates billing risk
- Cloud LLMs make low-spec hardware viable for AI agent development
- Simulated tools during development let you test flow before integrating real APIs
- Multi-file projects are far more maintainable than single-file notebooks
- Execution logs (JSON) provide audit trails and portfolio evidence

### Process

- Test each integration in isolation before chaining them
- Restart runtime between installation changes to avoid stale state
- Use terminal commands (New-Item) over GUI file creation to avoid path bugs
- Always verify .env is gitignored before first push

---

## 10. Next Steps

- [ ] Prepare client-facing templates (CLIENT_SETUP.md, scope of work, pricing sheet)
- [ ] Create Fiverr gig with portfolio screenshots
- [ ] Set up one-page Netlify landing site
- [ ] Apply to first 5 Fiverr Buyer Requests / Upwork proposals
- [ ] Add OAuth flow for client-friendly onboarding
- [ ] Consider paid VPS (Hetzner €3.79/mo) for 24/7 client deployments


*Document created: October 1, 2026*

*Project owner: suneelksr@gmail.com*

portfolio-evidence/
├── BUILD-LOG.md          ← new file
├── demos/
├── runs/
└── screenshots/
