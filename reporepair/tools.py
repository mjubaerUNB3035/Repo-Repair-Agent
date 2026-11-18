# tools.py

from reporepair.sandbox import run_in_sandbox

# Sandbox workdir
TESTBED = "/testbed"

# Search Code
def search_code(name: str, pattern: str) -> str:
    command = f"grep -rn '{pattern}' {TESTBED} --include=*.py"
    code, output = run_in_sandbox(name, command)
    return output

# Read File
def read_file(name: str, file_path: str) -> str:
    command = f"cat {file_path}"
    code, output = run_in_sandbox(name, command)
    return output

# Apply patch
def apply_patch(name: str, patch_text: str) -> str:
    command = "cat > /tmp/fix.patch << 'PATCH_EOF'\n"
    command += patch_text + "\nPATCH_EOF\n"
    command += f"cd {TESTBED} && git apply /tmp/fix.patch"
    code, output = run_in_sandbox(name, command)

    if code != 0:
        raise RuntimeError(output)
    return output

# Run Tests
def run_tests(name: str, test_command: str) -> str:
    command = f"cd {TESTBED} && {test_command}"
    code, output = run_in_sandbox(name, command)
    return output