# retrieve.py

import json
import urllib.request
import math

from reporepair.sandbox import run_in_sandbox
from reporepair.tools import read_file
from reporepair.config import load_settings
# Model
# EMBED_MODEL = "nomic-embed-text"

# Send Text - Get Number
def embed_text(text: str) -> list[float]:
    settings = load_settings()
    # Body Package
    body = {
        "model": settings.embed_model,
        "input": text,
    }
    # Text to Byte
    data = json.dumps(body).encode("utf-8")

    # Request line
    request = urllib.request.Request(
        settings.ollama_url + "/api/embed",
        data=data,
        headers={"Content-Type": "application/json"},
    )

    with urllib.request.urlopen(request, timeout=120) as response:
        # Byte to Text
        result = json.loads(response.read().decode("utf-8"))
    return result["embeddings"][0]

# Chunking
CHUNK_LINES = 40
CHUNK_STEP = 35


# Cut one file into parts
def chunk_file(path: str, text: str) -> list[dict]:
    lines = text.splitlines()
    chunks = []
    start = 0
    while start < len(lines):
        part = lines[start:start + CHUNK_LINES]
        chunk = {
            "path": path,
            "start_line": start + 1,
            "text": "\n".join(part),
        }
        chunks.append(chunk)
        start = start + CHUNK_STEP
    return chunks

# Fill the index from the box
def build_index(name: str, instance_id: str) -> list[dict]:
    settings = load_settings()
    # run sand box Gets all .py files
    code, output = run_in_sandbox(name, "find /testbed -name '*.py'")
    if code != 0:
        raise RuntimeError(output)
    index = []
    for line in output.splitlines():
        full = line.strip()
        if not full:
            continue
        # File name (9:)
        path = full[9:]
        text = read_file(name, path)
        chunks = chunk_file(path, text)
        for chunk in chunks:
            chunk["vector"] = embed_text(chunk["text"])
            index.append(chunk)

    index_path = settings.runs_dir / (instance_id + "_index.json")
    # Makes Folder
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(index, indent=2), encoding="utf-8")
    return index

# Compare two sets of numbers
def cosine(a: list[float], b: list[float]) -> float:
    dot = 0.0
    size_a = 0.0
    size_b = 0.0
    for i in range(len(a)):
        dot = dot + a[i] * b[i]
        size_a = size_a + a[i] * a[i]
        size_b = size_b + b[i] * b[i]
    if size_a == 0 or size_b == 0:
        return 0.0
    return dot / (math.sqrt(size_a) * math.sqrt(size_b))


# Find the closest parts for a question
def retrieve(index: list[dict], text: str) -> str:
    question = embed_text(text)
    scored = []
    for chunk in index:
        score = cosine(question, chunk["vector"])
        scored.append({"score": score, "chunk": chunk})
    parts = []
    for pick in range(5):
        best = None
        for item in scored:
            if best is None or item["score"] > best["score"]:
                best = item
        if best is None:
            break
        scored.remove(best)
        chunk = best["chunk"]
        head = chunk["path"] + " line " + str(chunk["start_line"])
        parts.append(head + "\n" + chunk["text"])
    return "\n\n".join(parts)


# Refresh one file in the index
def update_index(index, name, instance_id, path):
    settings = load_settings()
    # Read the file again
    text = read_file(name, path)
    # Drop the old parts
    kept = []
    for chunk in index:
        if chunk["path"] != path:
            kept.append(chunk)
    # Cut the new text
    chunks = chunk_file(path, text)
    # Number the new parts
    for chunk in chunks:
        chunk["vector"] = embed_text(chunk["text"])
        kept.append(chunk)
    # Save the index
    index_path = settings.runs_dir / (instance_id + "_index.json")
    # Makes Folder
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(kept, indent=2), encoding="utf-8")
    return kept
