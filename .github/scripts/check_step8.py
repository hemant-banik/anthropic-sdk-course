#!/usr/bin/env python3
"""Grading check for Step 8 — tool use (single round-trip).

Runs exercises/practice8_tools.py (live API calls through this project's
gateway) and checks stdout shows Claude requesting the get_weather tool,
then producing a final answer after the tool_result is sent back.
"""
import os
import subprocess
import sys
from pathlib import Path

EXERCISE_PATH = Path("exercises/practice8_tools.py")

REQUIRED_LABELS = ["stop_reason:", "tool name:", "tool input:", "final answer:"]


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
    if "tool_use_id" not in source:
        fail("Your script doesn't send back a tool_result with tool_use_id — that's required to complete the round-trip.")
    if "input_schema" not in source:
        fail("Your script doesn't define a tool with an input_schema.")

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

    if "stop_reason: tool_use" not in stdout:
        fail(f"Expected 'stop_reason: tool_use' — Claude should decide to call the tool. Got:\n{stdout}")

    if "get_weather" not in stdout:
        fail(f"Expected the tool name 'get_weather' to appear in stdout. Got:\n{stdout}")

    print("✅ PASS: tool use round-trip handled correctly.")
    print(stdout)


if __name__ == "__main__":
    main()
