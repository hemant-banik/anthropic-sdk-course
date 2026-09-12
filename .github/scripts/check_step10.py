#!/usr/bin/env python3
"""Grading check for Step 10 — vision with multiple images.

Runs exercises/practice10_vision.py (live API call through this project's
gateway) and checks stdout shows the "answer:" label with Claude correctly
distinguishing the red first image from the blue second image.
"""
import os
import subprocess
import sys
from pathlib import Path

EXERCISE_PATH = Path("exercises/practice10_vision.py")


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
    if source.count('"type": "image"') < 2:
        fail("Your script needs at least two image content blocks in the same message.")

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
    if "answer:" not in stdout:
        fail(f"Expected a line starting with 'answer:' in stdout. Got:\n{stdout}")

    lower = stdout.lower()
    if "red" not in lower:
        fail(f"Expected the reply to mention 'red' for the first image. Got stdout:\n{stdout}")
    if "blue" not in lower:
        fail(f"Expected the reply to mention 'blue' for the second image. Got stdout:\n{stdout}")

    print("✅ PASS: Claude correctly compared two images in one request.")
    print(stdout)


if __name__ == "__main__":
    main()
