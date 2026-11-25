#!/usr/bin/env python3
"""Roast Your Own Agent.

Writes one roast line -- a single line of at most 140 characters,
roasting my own AI agent -- to /output/entry.txt.

The roast is specific to how agents actually behave: the eager
agreement, the tool calls that go nowhere, and the confident delivery
of a plan nobody asked for.
"""

import os

LINE = (
    "My agent agrees with me instantly, opens twelve tools it never "
    "uses, then confidently ships the plan I never asked for."
)

MAX_CHARS = 140


def validate(line: str) -> None:
    if not line.strip():
        raise SystemExit("Invalid line: entry must be non-empty.")
    if line != line.strip():
        raise SystemExit(
            "Invalid line: entry must not have leading or trailing whitespace."
        )
    if len(line) > MAX_CHARS:
        raise SystemExit(
            f"Invalid line: {len(line)} characters, over the "
            f"{MAX_CHARS} limit."
        )
    if "\n" in line or "\r" in line:
        raise SystemExit(
            "Invalid line: entry must be a single line with no newline characters."
        )
    line.encode("utf-8")


def main() -> None:
    validate(LINE)
    output_path = os.environ.get("OUTPUT_PATH", "/output/entry.txt")
    parent = os.path.dirname(output_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    expected = LINE.encode("utf-8")
    with open(output_path, "wb") as f:
        f.write(expected)
    with open(output_path, "rb") as f:
        written = f.read()
    if written != expected:
        raise SystemExit(
            "Write verification failed: entry file bytes do not match the line."
        )
    print(f"wrote {len(LINE)} chars to {output_path}")


if __name__ == "__main__":
    main()
