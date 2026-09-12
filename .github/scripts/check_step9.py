#!/usr/bin/env python3
"""Grading check for Step 9 — extended thinking.

Runs exercises/practice9_thinking.py (live API call through this project's
gateway) and checks stdout shows a nonempty thinking block plus the correct
final answer (918 = 27 * 34).
"""
import os
import re
import subprocess
import sys
from pathlib import Path

EXERCISE_PATH = Path("exercises/practice9_thinking.py")

REQUIRED_LABELS = ["has thinking block:", "thinking length:", "answer:"]


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
    if '"thinking"' not in source and "'thinking'" not in source:
        fail("Your script doesn't pass thinking={'type': 'enabled', ...} to enable extended thinking.")
    if "budget_tokens" not in source:
        fail("Your script doesn't set budget_tokens — required by the thinking parameter.")

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

    if "has thinking block: True" not in stdout:
        fail(f"Expected 'has thinking block: True'. Got stdout:\n{stdout}")

    match = re.search(r"thinking length:\s*(\d+)", stdout)
    if not match or int(match.group(1)) <= 0:
        fail(f"Expected 'thinking length:' to be greater than 0. Got stdout:\n{stdout}")

    if "918" not in stdout:
        fail(f"Expected the answer to contain '918' (27 * 34). Got stdout:\n{stdout}")

    print("✅ PASS: extended thinking enabled and both block types read correctly.")
    print(stdout)


if __name__ == "__main__":
    main()
