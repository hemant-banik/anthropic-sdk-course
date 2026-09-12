#!/usr/bin/env python3
"""Grading check for Step 4 — message roles & multi-turn conversation.

Runs exercises/practice4_multiturn.py (live API calls through this project's
gateway) and checks stdout shows Claude remembering the name from turn 1
when asked about it in turn 2, plus the expected "Messages in list:" count.
"""
import os
import subprocess
import sys
from pathlib import Path

EXERCISE_PATH = Path("exercises/practice4_multiturn.py")

REQUIRED_LABELS = ["Turn 1:", "Turn 2:", "Messages in list:"]


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
    if ".append(" not in source:
        fail("Your script doesn't call .append() on the messages list — multi-turn requires resending history.")

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

    if "zara" not in stdout.lower():
        fail(f"Expected Turn 2's reply to mention the name 'Zara'. Got stdout:\n{stdout}")

    if "Messages in list: 4" not in stdout:
        fail(f"Expected 'Messages in list: 4' (2 user + 2 assistant turns). Got stdout:\n{stdout}")

    print("✅ PASS: multi-turn conversation correctly remembered context across turns.")
    print(stdout)


if __name__ == "__main__":
    main()
