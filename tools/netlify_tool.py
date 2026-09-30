"""
tools/netlify_tool.py — Netlify site creation tool.

Wraps the Netlify REST API `POST /api/v1/sites` endpoint in a
CrewAI-compatible tool that agents can call.
"""

import requests
from crewai.tools import tool
from config import config


@tool("Netlify Deploy Tool")
def deploy_to_netlify(site_name: str) -> str:
    """
    Creates a real Netlify site on the authenticated user's account.

    Args:
        site_name: The desired subdomain for the site
                   (e.g., "my-demo" creates "my-demo.netlify.app").

    Returns:
        A status string indicating success (with live URL) or failure.
    """
    token = config.NETLIFY_AUTH_TOKEN
    if not token:
        return "❌ [Netlify] NETLIFY_AUTH_TOKEN is not configured."

    url = "https://api.netlify.com/api/v1/sites"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {"name": site_name}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code in (200, 201):
            data = response.json()
            live_url = data.get("ssl_url") or data.get("url") or "(no URL returned)"
            return f"🚀 [Netlify] Site created: {live_url}"
        if response.status_code == 422:
            # Most likely subdomain already taken
            errors = response.json().get("errors", response.text)
            return f"❌ [Netlify] Failed (422 — likely name collision): {errors}"
        return f"❌ [Netlify] Failed ({response.status_code}): {response.text}"
    except requests.Timeout:
        return "❌ [Netlify] Request timed out after 30 seconds."
    except Exception as e:
        return f"❌ [Netlify] Connection error: {e}"