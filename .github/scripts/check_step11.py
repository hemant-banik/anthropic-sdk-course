#!/usr/bin/env python3
"""Grading check for Step 11 — PDF support (document content block).

Runs exercises/practice11_pdf.py (live API call through this project's
gateway) and checks stdout shows the PDF was created and Claude correctly
read the secret code (4471) straight out of the PDF text.
"""
import os
import subprocess
import sys
from pathlib import Path

EXERCISE_PATH = Path("exercises/practice11_pdf.py")


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
    if '"type": "document"' not in source:
        fail("Your script doesn't include a document content block ('type': 'document').")
    if "application/pdf" not in source:
        fail("Your script doesn't set media_type to 'application/pdf'.")

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
    if "pdf created: True" not in stdout:
        fail(f"Expected 'pdf created: True' in stdout. Got:\n{stdout}")
    if "answer:" not in stdout:
        fail(f"Expected a line starting with 'answer:' in stdout. Got:\n{stdout}")
    if "4471" not in stdout:
        fail(f"Expected the answer to contain the secret code '4471'. Got stdout:\n{stdout}")

    print("✅ PASS: Claude correctly read the contents of the base64-encoded PDF.")
    print(stdout)


if __name__ == "__main__":
    main()
