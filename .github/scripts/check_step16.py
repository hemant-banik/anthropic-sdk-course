#!/usr/bin/env python3
"""Grading check for Step 16 — error handling with APIStatusError.

Runs exercises/practice16_error_handling.py (live API call through this
project's gateway using a deliberately invalid model name) and checks
stdout has the labeled error_type/error_message output, proving the
exception was caught rather than crashing the script.
"""
import os
import subprocess
import sys
from pathlib import Path

EXERCISE_PATH = Path("exercises/practice16_error_handling.py")

REQUIRED_LABELS = ["error_type:", "error_message:"]


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
    if "except" not in source or "anthropic." not in source:
        fail("Your script doesn't appear to catch an anthropic exception type.")

    result = subprocess.run(
        [sys.executable, str(EXERCISE_PATH)],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        fail(
            "Your script raised an uncaught error when run (the exception "
            "should have been caught, not crash the script):\n"
            f"--- stdout ---\n{result.stdout}\n"
            f"--- stderr ---\n{result.stderr}"
        )

    stdout = result.stdout
    if "No error was raised" in stdout:
        fail("The API call succeeded instead of failing — use an invalid model name so an error is actually raised.")

    for label in REQUIRED_LABELS:
        if label not in stdout:
            fail(f"Expected a line starting with '{label}' in stdout. Got:\n{stdout}")

    print("✅ PASS: error was deliberately triggered and caught correctly.")
    print(stdout)


if __name__ == "__main__":
    main()
