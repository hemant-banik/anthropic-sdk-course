#!/usr/bin/env python3
"""Grading check for Step 13 — count tokens with client.messages.count_tokens().

Runs exercises/practice13_token_counting.py (live API call through this
project's gateway) and checks stdout has both expected labeled lines, that
the long message counted more tokens than the short one, and that the
client setup still uses this project's real pattern (load_dotenv +
ICA_API_KEY + base_url).
"""
import os
import re
import subprocess
import sys
from pathlib import Path

EXERCISE_PATH = Path("exercises/practice13_token_counting.py")

REQUIRED_LABELS = ["short_tokens:", "long_tokens:"]


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
    if "count_tokens" not in source:
        fail("Your script doesn't call count_tokens() — that's the whole point of this step!")

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

    short_match = re.search(r"short_tokens:\s*(\d+)", stdout)
    long_match = re.search(r"long_tokens:\s*(\d+)", stdout)
    if not short_match or not long_match:
        fail(f"Couldn't parse integer token counts out of stdout:\n{stdout}")

    short_tokens = int(short_match.group(1))
    long_tokens = int(long_match.group(1))
    if long_tokens <= short_tokens:
        fail(
            f"Expected long_tokens ({long_tokens}) to be greater than "
            f"short_tokens ({short_tokens}) — the long message should count more tokens."
        )

    print("✅ PASS: token counting works correctly.")
    print(stdout)


if __name__ == "__main__":
    main()
