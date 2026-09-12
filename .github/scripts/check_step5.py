#!/usr/bin/env python3
"""Grading check for Step 5 — content blocks: text + image input (base64).

Runs exercises/practice5_image.py (live API call through this project's
gateway) and checks stdout shows the expected "color:" label with Claude
correctly identifying the solid-red test image.
"""
import os
import subprocess
import sys
from pathlib import Path

EXERCISE_PATH = Path("exercises/practice5_image.py")


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
    if '"type": "image"' not in source:
        fail("Your script doesn't include an image content block ('type': 'image').")
    if "base64" not in source:
        fail("Your script doesn't appear to base64-encode the image data.")

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
    if "color:" not in stdout:
        fail(f"Expected a line starting with 'color:' in stdout. Got:\n{stdout}")
    if "red" not in stdout.lower():
        fail(f"Expected the reply to mention 'red'. Got stdout:\n{stdout}")

    print("✅ PASS: Claude correctly identified the base64-encoded image.")
    print(stdout)


if __name__ == "__main__":
    main()
