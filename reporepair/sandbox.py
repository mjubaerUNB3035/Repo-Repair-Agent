# Sandbox

import subprocess

# Docker
DEFAULT_IMAGE = "python:3.13-slim"
WORKDIR = "/testbed"

# Container name
def container_name(instance_id: str) -> str:
    name = "reporepair-" + instance_id
    return name.replace("_", "-").lower()

# Run docker command
def run_docker(args: list[str], timeout: int = 600) -> tuple[int, str]:
    result = subprocess.run(
        ["docker"] + args,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    output = result.stdout + result.stderr
    return result.returncode, output

# Start sandbox
def start_sandbox(instance_id: str, image: str = DEFAULT_IMAGE) -> str:
    name = container_name(instance_id)
    run_docker(["rm", "-f", name]) # Delete File
    code, output = run_docker(
        ["run", "-dit", "--name", name, "-w", WORKDIR, image, "sleep", "infinity"]
    )
    # Error
    if code != 0:
        raise RuntimeError(output)
    return name

# Run in sandbox
def run_in_sandbox(name: str, command: str, timeout: int = 600) -> tuple[int, str]:
    return run_docker(["exec", name, "sh", "-c", command], timeout=timeout)


# Stop sandbox
def stop_sandbox(name: str) -> None:
    run_docker(["rm", "-f", name])