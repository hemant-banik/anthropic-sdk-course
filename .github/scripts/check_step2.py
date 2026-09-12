#!/usr/bin/env python3
"""Grading check for Step 2 — first messages.create() call.

Runs exercises/practice_message.py for real (this step DOES call the live
Anthropic API through this project's gateway, so ICA_API_KEY must be set)
and checks the reply contains "4" (the answer to "What is 2 + 2?").
"""
import os
import subprocess
import sys
from pathlib import Path

EXERCISE_PATH = Path("exercises/practice_message.py")


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
    for required in ("model=", "max_tokens=", "messages="):
        if required not in source:
            fail(f"Your call to messages.create() is missing the '{required}' parameter.")

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

    if "4" not in result.stdout:
        fail(f"Expected the reply to mention '4'. Got stdout:\n{result.stdout}")

    print("✅ PASS: messages.create() call succeeded and returned the right answer.")
    print(result.stdout)


if __name__ == "__main__":
    main()
