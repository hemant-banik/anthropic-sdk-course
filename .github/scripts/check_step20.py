#!/usr/bin/env python3
"""Grading check for Step 20 — web search tool (server-side tool).

Runs exercises/practice20_web_search.py (live API call through this
project's gateway) using the web_search_20250305 server tool, and checks
stdout has both the labeled block_types line and the answer line.
"""
import os
import subprocess
import sys
from pathlib import Path

EXERCISE_PATH = Path("exercises/practice20_web_search.py")

TOOL_TYPE = "web_search_20250305"


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
    if TOOL_TYPE not in source:
        fail(f"Your script doesn't use tool type '{TOOL_TYPE}' — that's the exact server tool string required.")
    if "web_search" not in source:
        fail("Your script doesn't reference the web_search tool name.")

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
    if "block_types:" not in stdout:
        fail(f"Expected a line starting with 'block_types:' in stdout. Got:\n{stdout}")
    if "answer:" not in stdout:
        fail(f"Expected a line starting with 'answer:' in stdout. Got:\n{stdout}")

    print("✅ PASS: web search tool ran and returned a cited answer.")
    print(stdout)


if __name__ == "__main__":
    main()
