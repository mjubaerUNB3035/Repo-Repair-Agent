# agent.py

import json
import urllib.request

from reporepair.config import load_settings
from reporepair.state import AgentState


# Ask model
def ask_model(prompt: str) -> str:
    settings = load_settings()
    body = {
        "model": settings.model_name,
        "prompt": prompt,
        "stream": False,
    }
    data = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        settings.ollama_url + "/api/generate",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=300) as response:
        result = json.loads(response.read().decode("utf-8"))
    return result["response"]


# Build prompt
def build_prompt(state: AgentState) -> str:
    lines = []
    lines.append("You are a code repair agent. Fix the issue below.")
    lines.append("Reply with exactly one action:")
    lines.append("SEARCH <word>  to search the code")
    lines.append("READ <path>  to read one file, path from the repo root")
    lines.append("PATCH  then the full patch text on the following lines")
    lines.append("DONE  when the fix is finished")
    lines.append("")
    lines.append("Issue: " + state["issue_text"])
    lines.append("Files found so far: " + ", ".join(state["found_files"]))
    lines.append("Last test output: " + state["test_output"][-500:])
    return "\n".join(lines)


# Parse action
def parse_action(text: str) -> tuple[str, str]:
    lines = text.strip().splitlines()
    if not lines:
        return "unknown", ""
    first = lines[0].strip()
    if first.startswith("SEARCH"):
        return "search", first[6:].strip()
    if first.startswith("READ"):
        return "read", first[4:].strip()
    if first.startswith("PATCH"):
        return "patch", "\n".join(lines[1:]).strip()
    if first.startswith("DONE"):
        return "done", ""
    return "unknown", first
