# Client Setup Guide

Welcome, and thank you for your business. This guide walks you through what was built for you, what you now own, and how to use it.

## What Was Delivered

An automated multi-agent worker that provisions infrastructure across your own accounts on three platforms:

- **Retell AI** — a voice agent for handling calls
- **GitHub** — a repository to host your code
- **Netlify** — a live website for your project

The worker runs from your own machine, uses your own API keys, and creates artifacts inside your own accounts. There is no middleman service, no ongoing subscription to me, and no dependency on my infrastructure.

## Your Accounts

Everything created for you lives in **your** accounts, not mine. You have full control and can access, modify, or delete anything at any time.

| Service | What to Look For | Login URL |
|---|---|---|
| **Retell AI** | Agents section — your voice agent | https://www.retellai.com |
| **GitHub** | Repositories list — your project repo | https://github.com |
| **Netlify** | Sites dashboard — your live website | https://app.netlify.com |

## Your API Keys

The following API keys are used by the worker. They belong to **you** and are stored in a local `.env` file on the machine where the worker runs:

| Key | Purpose | Where to Regenerate |
|---|---|---|
| `GROQ_API_KEY` | Powers the AI reasoning | https://console.groq.com/keys |
| `RETELL_API_KEY` | Creates voice agents | Retell dashboard, API Keys |
| `GITHUB_TOKEN` | Creates repositories | https://github.com/settings/tokens |
| `NETLIFY_AUTH_TOKEN` | Deploys websites | https://app.netlify.com/user/applications |

**Security note:** These keys are stored in the `.env` file, which is excluded from Git. Never commit that file. If a key is ever exposed, regenerate it from the service dashboard immediately.

## How to Run the Worker

If you need to re-run the worker to create additional resources or update existing ones:

```bash
cd /path/to/voice-multiagent-worker
python main.py
```
The worker typically takes 1 to 2 minutes to complete. It will:
1. Load your API keys
2. Build the two specialized agents
3. Execute the tasks you defined
4. Return URLs for any artifacts it creates
5. Save a log to `logs/run_YYYYMMDD_HHMMSS.json`

## How to Change What It Creates

All defaults are in the `.env` file. To create a new voice agent, repo, or site, edit these lines:

```
RETELL_AGENT_NAME=Your New Voice Agent Name
GITHUB_REPO_NAME=your-new-repo-name
NETLIFY_SITE_NAME=your-new-site-name
```

Save the file and run `python main.py` again.

**Important:** GitHub repo names and Netlify site names must be globally unique. If the worker returns a "name already exists" error, pick a different name.

## Logs and Audit Trail

Every run writes a JSON log to the `logs/` folder. Each log contains:

- Timestamp of the run
- The final result (URLs, agent IDs)
- Agent and task counts
- The model used

These logs are your audit trail. They prove what was created and when.

## What You Own

- The Python source code
- All API keys (under your accounts)
- The Retell voice agent
- The GitHub repository
- The Netlify website
- All execution logs

## What You Do Not Own

- The domain `voice-multiagent-worker` (this is a demo reference)
- Any future updates to the underlying framework (CrewAI, LiteLLM)
- Third-party service uptime (Retell, GitHub, Netlify, Groq)

## What If Something Breaks

The system depends on four external services. If any of them changes their API, the worker may need adjustment. Typical scenarios:

| Issue | Likely Cause | Action |
|---|---|---|
| Worker fails with "Invalid API Key" | Key expired or rotated | Regenerate from the service dashboard |
| Retell says "Invalid response engine" | Retell API changed | Contact me for an update |
| GitHub returns 422 | Repo name already used | Change name in `.env` |
| Netlify returns 422 | Site name already used | Change name in `.env` |
| Groq returns "cache_breakpoint unsupported" | LiteLLM patch missing | Restart Python; the patch is applied at startup |

## Support and Maintenance

If you are on a maintenance plan, I will:

- Monitor for API changes in Retell, GitHub, Netlify, or Groq
- Update the code if any service changes its interface
- Respond to issues within 1 business day

If you are on a delivery-only plan, you can reach me for hourly or per-incident support:

- **Email:** suneelksr@gmail.com
- **Response time:** Within 2 business days

## Common Customizations

Want something different from what was delivered? Common requests include:

- **Different voice** — change the Retell voice ID in `tools/retell_tool.py`
- **Different prompt** — edit the `general_prompt` string in `tools/retell_tool.py`
- **Extra services** — add a new file in `tools/` following the existing pattern
- **Scheduled runs** — deploy the worker to a VPS and add a cron job (I can help)

## Questions

If anything here is unclear, or you want a walkthrough of any part of the system, reach out. I would rather answer a small question now than have you stuck with an unclear system later.

Thank you again for your business.

---

*This guide was written specifically for your delivery. Keep it with your project files for future reference.*