#!/usr/bin/env python3
"""Grading check for Step 12 — prompt caching.

Runs exercises/practice12_caching.py (two live API calls through this
project's gateway) and checks stdout shows the first call writing to the
cache and the second call reading from it.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

EXERCISE_PATH = Path("exercises/practice12_caching.py")

REQUIRED_LABELS = [
    "first cache_creation_input_tokens:",
    "first cache_read_input_tokens:",
    "second cache_creation_input_tokens:",
    "second cache_read_input_tokens:",
]


def fail(msg: str) -> None:
    print(f"❌ FAIL: {msg}")
    sys.exit(1)


def main() -> None:
    if not os.environ.get("ICA_API_KEY"):
        fail(
            "ICA_API_KEY is not set. Add it as a repo secret: "
            "Settings -> Secrets and variables -> Actions -> New repository secret."
        )

    if not EXERCISE_PATH.exists():
        fail(f"{EXERCISE_PATH} does not exist. Create it as instructed in the issue.")

    source = EXERCISE_PATH.read_text()
    if "load_dotenv()" not in source:
        fail("Your script doesn't call load_dotenv() — this project loads the key from a .env file.")
    if "ICA_API_KEY" not in source:
        fail("Your script doesn't reference ICA_API_KEY — that's the key name this project uses.")
    if "base_url=" not in source:
        fail("Your script doesn't set base_url= — this project routes requests through a custom gateway.")
    if "cache_control" not in source:
        fail("Your script doesn't set cache_control on any block — that's what enables caching.")
    if "ephemeral" not in source:
        fail("Your script doesn't use {'type': 'ephemeral'} for cache_control.")

    result = subprocess.run(
        [sys.executable, str(EXERCISE_PATH)],
        capture_output=True,
        text=True,
        timeout=90,
    )
    if result.returncode != 0:
        fail(
            "Your script raised an error when run:\n"
            f"--- stdout ---\n{result.stdout}\n"
            f"--- stderr ---\n{result.stderr}"
        )

    stdout = result.stdout
    for label in REQUIRED_LABELS:
        if label not in stdout:
            fail(f"Expected a line starting with '{label}' in stdout. Got:\n{stdout}")

    creation_match = re.search(r"first cache_creation_input_tokens:\s*(\d+)", stdout)
    if not creation_match or int(creation_match.group(1)) <= 0:
        fail(f"Expected 'first cache_creation_input_tokens:' to be greater than 0 (the cache write). Got:\n{stdout}")

    read_match = re.search(r"second cache_read_input_tokens:\s*(\d+)", stdout)
    if not read_match or int(read_match.group(1)) <= 0:
        fail(f"Expected 'second cache_read_input_tokens:' to be greater than 0 (the cache hit). Got:\n{stdout}")

    print("✅ PASS: prompt caching wrote on the first call and was read on the second call.")
    print(stdout)


if __name__ == "__main__":
    main()
