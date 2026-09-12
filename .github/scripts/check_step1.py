#!/usr/bin/env python3
"""Grading check for Step 1 — Install SDK & create a client.

Runs the learner's exercises/practice1.py and verifies stdout contains the
two expected lines. Exits 0 on pass, 1 on fail (with a human-readable
reason printed to stdout so it shows up in the Actions log and, if needed,
in the issue comment).
"""
import subprocess
import sys
from pathlib import Path

EXERCISE_PATH = Path("exercises/practice1.py")


def fail(msg: str) -> None:
    print(f"❌ FAIL: {msg}")
    sys.exit(1)


def main() -> None:
    if not EXERCISE_PATH.exists():
        fail(f"{EXERCISE_PATH} does not exist. Create it as instructed in the issue.")

    source = EXERCISE_PATH.read_text()
    if "load_dotenv()" not in source:
        fail("Your script doesn't call load_dotenv() — this project loads the key from a .env file.")
    if "ICA_API_KEY" not in source:
        fail("Your script doesn't reference ICA_API_KEY — that's the key name this project uses.")
    if "base_url=" not in source:
        fail("Your script doesn't set base_url= — this project routes requests through a custom gateway.")

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
    if "SDK version:" not in stdout:
        fail("Expected a line starting with 'SDK version:' in stdout.")
    if "Client type: Anthropic" not in stdout:
        fail("Expected a line 'Client type: Anthropic' in stdout.")

    print("✅ PASS: SDK installed and client created correctly.")
    print(stdout)


if __name__ == "__main__":
    main()
