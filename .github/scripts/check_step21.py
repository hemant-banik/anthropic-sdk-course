#!/usr/bin/env python3
"""Grading check for Step 21 — Bedrock/Vertex client variants (FINAL STEP).

Unlike every other checker in this course, this one does NOT run the
learner's script as a subprocess and does NOT require ICA_API_KEY — the
whole point of this step is a conceptual, text-based comparison that most
learners can complete without real AWS/GCP credentials. We only validate
the source text: both client class names must appear, and each must be
accompanied by an explanatory comment about when to use it.
"""
import re
import sys
from pathlib import Path

EXERCISE_PATH = Path("exercises/practice21_bedrock_vertex.py")

REQUIRED_CLASSES = ["AnthropicBedrock", "AnthropicVertex"]


def fail(msg: str) -> None:
    print(f"❌ FAIL: {msg}")
    sys.exit(1)


def has_nearby_explanatory_comment(source: str, class_name: str) -> bool:
    """Look for a '#' comment line near (within 6 lines above) a class usage
    that contains words suggesting a "when to use this" explanation."""
    lines = source.splitlines()
    for i, line in enumerate(lines):
        if class_name in line:
            window = lines[max(0, i - 6):i + 1]
            for w_line in window:
                stripped = w_line.strip()
                if stripped.startswith("#"):
                    lower = stripped.lower()
                    if "use" in lower and ("when" in lower or "if" in lower or "want" in lower):
                        return True
    return False


def main() -> None:
    # NOTE: intentionally no ICA_API_KEY check here — this step makes no
    # live API call, unlike every other step in the course.

    if not EXERCISE_PATH.exists():
        fail(f"{EXERCISE_PATH} does not exist. Create it as instructed in the issue.")

    source = EXERCISE_PATH.read_text()

    for class_name in REQUIRED_CLASSES:
        if class_name not in source:
            fail(f"Your script doesn't reference {class_name} — both client classes are required.")

    if "import" not in source or not re.search(r"from\s+anthropic\s+import", source):
        fail("Your script doesn't import from the anthropic package (expected 'from anthropic import ...').")

    for class_name in REQUIRED_CLASSES:
        if not has_nearby_explanatory_comment(source, class_name):
            fail(
                f"Couldn't find an explanatory '# ... use ... when/if/want ...' comment "
                f"near your {class_name} usage. Add a comment explaining when you'd "
                f"reach for {class_name} specifically."
            )

    print("✅ PASS: script demonstrates both client variants with clear usage comments.")
    print(f"Found classes: {', '.join(REQUIRED_CLASSES)}")


if __name__ == "__main__":
    main()
