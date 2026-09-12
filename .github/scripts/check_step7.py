#!/usr/bin/env python3
"""Grading check for Step 7 — structured / JSON output.

Runs exercises/practice7_json.py (live API call through this project's
gateway) and checks stdout shows the raw text plus successfully parsed
'name'/'age' fields with the correct Python type for age.
"""
import os
import subprocess
import sys
from pathlib import Path

EXERCISE_PATH = Path("exercises/practice7_json.py")

REQUIRED_LABELS = ["raw:", "parsed name:", "parsed age:", "age type:"]


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
    if "json.loads(" not in source:
        fail("Your script doesn't call json.loads() to parse Claude's reply.")

    result = subprocess.run(
        [sys.executable, str(EXERCISE_PATH)],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        fail(
            "Your script raised an error when run (often a JSON parsing error — "
            "print raw_text to debug what Claude actually returned):\n"
            f"--- stdout ---\n{result.stdout}\n"
            f"--- stderr ---\n{result.stderr}"
        )

    stdout = result.stdout
    for label in REQUIRED_LABELS:
        if label not in stdout:
            fail(f"Expected a line starting with '{label}' in stdout. Got:\n{stdout}")

    if "age type: int" not in stdout:
        fail(f"Expected 'age type: int' — json.loads() should parse age as an integer. Got:\n{stdout}")

    print("✅ PASS: JSON output requested and parsed correctly.")
    print(stdout)


if __name__ == "__main__":
    main()
