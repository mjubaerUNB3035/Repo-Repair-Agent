# Load SWE-Bench Lite Instance
import json
from datasets import load_dataset
from reporepair.config import project_root

DATASET_NAME = "princeton-nlp/SWE-bench_Lite"

# Load Pilot-id from pilot_instances.txt.
def load_pilot_ids() -> list[str]:
    path = project_root() / "data" / "pilot_instances.txt"
    lines = path.read_text(encoding="utf-8").splitlines()
    ids = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            ids.append(line)
    return ids

# Turn Raw test to List
def parse_test_list(raw) -> list[str]:
    if isinstance(raw, list):
        return raw
    return json.loads(raw)

# Load one instance by id -> Return dict 
def get_instance(instance_id: str) -> dict:
    dataset = load_dataset(DATASET_NAME, split="test")
    for row in dataset:
        if row["instance_id"] == instance_id:
            return {
                "instance_id": row["instance_id"],
                "repo": row["repo"],
                "base_commit": row["base_commit"],
                "issue_text": row["problem_statement"],
                "fail_to_pass": parse_test_list(row["FAIL_TO_PASS"]),
                "pass_to_pass": parse_test_list(row["PASS_TO_PASS"]),
            }
    raise ValueError(f"Instance not found in SWE-bench Lite: {instance_id}")
