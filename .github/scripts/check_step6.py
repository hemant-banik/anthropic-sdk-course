#!/usr/bin/env python3
"""Grading check for Step 6 — streaming responses.

Runs exercises/practice6_streaming.py (live API call through this project's
gateway, streamed) and checks stdout has the "streaming:", "stop_reason:",
and "chars streamed:" labels, with a nonzero character count.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

EXERCISE_PATH = Path("exercises/practice6_streaming.py")

REQUIRED_LABELS = ["streaming:", "stop_reason:", "chars streamed:"]


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
    if "messages.stream(" not in source:
        fail("Your script doesn't call client.messages.stream() — use the streaming method, not .create().")
    if "text_stream" not in source:
        fail("Your script doesn't iterate stream.text_stream.")

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

    match = re.search(r"chars streamed:\s*(\d+)", stdout)
    if not match or int(match.group(1)) <= 0:
        fail(f"Expected 'chars streamed:' to be greater than 0. Got stdout:\n{stdout}")

    if "stop_reason: end_turn" not in stdout:
        fail(f"Expected 'stop_reason: end_turn' in stdout. Got:\n{stdout}")

    print("✅ PASS: streaming response handled correctly.")
    print(stdout)


if __name__ == "__main__":
    main()
