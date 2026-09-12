#!/usr/bin/env python3
"""Grading check for Step 3 — inspect the full response object.

Runs exercises/practice_inspect.py (live API call) and checks stdout has
all six expected labeled lines, and that the id/role/stop_reason values
look right.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

EXERCISE_PATH = Path("exercises/practice_inspect.py")

REQUIRED_LABELS = ["id:", "model:", "role:", "stop_reason:", "usage:", "text:"]


def fail(msg: str) -> None:
    print(f"❌ FAIL: {msg}")
    sys.exit(1)


def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        fail(
            "ANTHROPIC_API_KEY is not set. Add it as a repo secret: "
            "Settings -> Secrets and variables -> Actions -> New repository secret."
        )

    if not EXERCISE_PATH.exists():
        fail(f"{EXERCISE_PATH} does not exist. Create it as instructed in the issue.")

    result = subprocess.run(
        [sys.executable, str(EXERCISE_PATH)],
        capture_output=True,
        text=True,
        timeout=60,
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

    if not re.search(r"id:\s*msg_", stdout):
        fail("Expected the printed 'id:' to start with 'msg_'.")
    if "role: assistant" not in stdout:
        fail("Expected 'role: assistant' in stdout.")

    print("✅ PASS: response object inspected correctly.")
    print(stdout)


if __name__ == "__main__":
    main()
