#!/usr/bin/env python3
"""Grading check for Step 18 — Files API upload + reference by file_id.

Runs exercises/practice18_files_api.py (live API call through this
project's gateway) and checks stdout has both expected labeled lines: a
real file_id and a non-empty summary referencing the uploaded content.
"""
import os
import subprocess
import sys
from pathlib import Path

EXERCISE_PATH = Path("exercises/practice18_files_api.py")

REQUIRED_LABELS = ["file_id:", "summary:"]


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
    if "files.upload" not in source:
        fail("Your script doesn't call client.files.upload() — that's the whole point of this step!")
    if "file_id" not in source:
        fail("Your script doesn't reference file_id in a document content block.")

    result = subprocess.run(
        [sys.executable, str(EXERCISE_PATH)],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        fail(
            "Your script raised an error when run (see the step's troubleshooting "
            "note if this is a gateway Files API limitation):\n"
            f"--- stdout ---\n{result.stdout}\n"
            f"--- stderr ---\n{result.stderr}"
        )

    stdout = result.stdout
    for label in REQUIRED_LABELS:
        if label not in stdout:
            fail(f"Expected a line starting with '{label}' in stdout. Got:\n{stdout}")

    if "file_id: file_" not in stdout and "file_id:file_" not in stdout:
        fail(f"Expected file_id to start with 'file_'. Got stdout:\n{stdout}")

    print("✅ PASS: file uploaded and referenced by file_id successfully.")
    print(stdout)


if __name__ == "__main__":
    main()
