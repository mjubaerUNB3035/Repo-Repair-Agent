# state.py

from typing import TypedDict

# SWE-bench Lite
class AgentState(TypedDict):

    # Issue
    instance_id: str
    repo: str
    base_commit: str
    issue_text: str

    # In Progress Work
    found_files: list[str]
    patch: str
    test_output: str

    # Limits
    steps_used: int
    retries_used: int

    # Result
    status: str
    error: str


# Fresh state
def new_state(instance_id: str, repo: str, base_commit: str, issue_text: str) -> AgentState:
    return AgentState(
        instance_id=instance_id,
        repo=repo,
        base_commit=base_commit,
        issue_text=issue_text,
        found_files=[],
        patch="",
        test_output="",
        steps_used=0,
        retries_used=0,
        status="new",
        error="",
    )
