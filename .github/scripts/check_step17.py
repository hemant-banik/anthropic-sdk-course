#!/usr/bin/env python3
"""Grading check for Step 17 — compare model + stop_reason across models.

Runs exercises/practice17_models_available.py (live API calls through this
project's gateway to at least 2 different model strings) and checks stdout
labels the model name and stop_reason for each call.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

EXERCISE_PATH = Path("exercises/practice17_models_available.py")


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
    model_matches = re.findall(r"model:\s*(\S+)", stdout)
    stop_reason_matches = re.findall(r"stop_reason:\s*(\S+)", stdout)

    if len(model_matches) < 2:
        fail(
            "Expected at least 2 lines starting with 'model:' (one per model "
            f"tested). Got {len(model_matches)} in stdout:\n{stdout}"
        )
    if len(stop_reason_matches) < 2:
        fail(
            "Expected at least 2 lines starting with 'stop_reason:' (one per "
            f"model tested). Got {len(stop_reason_matches)} in stdout:\n{stdout}"
        )
    if len(set(model_matches)) < 2:
        fail(
            f"Expected at least 2 DIFFERENT model names printed, got: {model_matches}. "
            "Use 2-3 different model= strings."
        )

    print("✅ PASS: compared model + stop_reason across multiple models.")
    print(stdout)


if __name__ == "__main__":
    main()
