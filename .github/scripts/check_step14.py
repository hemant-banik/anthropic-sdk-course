#!/usr/bin/env python3
"""Grading check for Step 14 — Batch API (create, poll, retrieve results).

Runs exercises/practice14_batch_api.py (live API calls through this
project's gateway) and checks stdout has the expected labeled lines,
including a final tally showing both requests succeeded. Batches are
async server-side, so this checker allows extra time for polling.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

EXERCISE_PATH = Path("exercises/practice14_batch_api.py")

REQUIRED_LABELS = ["batch_id:", "initial_status:", "succeeded:", "errored:"]

# Batches usually finish in minutes, but give CI plenty of headroom.
TIMEOUT_SECONDS = 600


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
    if "batches.create" not in source:
        fail("Your script doesn't call messages.batches.create() — that's the whole point of this step!")
    if "batches.retrieve" not in source:
        fail("Your script doesn't poll with messages.batches.retrieve() — you need to check batch status.")
    if "batches.results" not in source:
        fail("Your script doesn't call messages.batches.results() — you need to retrieve the batch results.")

    try:
        result = subprocess.run(
            [sys.executable, str(EXERCISE_PATH)],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        fail(
            f"Your script did not finish within {TIMEOUT_SECONDS} seconds. "
            "Batches usually finish within minutes — if this keeps happening, re-run the workflow."
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

    if not re.search(r"batch_id:\s*msgbatch_", stdout):
        fail("Expected the printed 'batch_id:' to start with 'msgbatch_'.")

    succeeded_match = re.search(r"succeeded:\s*(\d+)", stdout)
    errored_match = re.search(r"errored:\s*(\d+)", stdout)
    if not succeeded_match or not errored_match:
        fail(f"Couldn't parse succeeded/errored counts out of stdout:\n{stdout}")

    succeeded = int(succeeded_match.group(1))
    errored = int(errored_match.group(1))
    if succeeded < 2:
        fail(f"Expected both batch requests to succeed (succeeded: 2), got succeeded: {succeeded}.")
    if errored != 0:
        fail(f"Expected 0 errored requests, got errored: {errored}.\n{stdout}")

    print("✅ PASS: batch created, polled, and results retrieved correctly.")
    print(stdout)


if __name__ == "__main__":
    main()
