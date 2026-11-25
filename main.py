#!/usr/bin/env python3
"""Roast Your Own Agent.

Writes one roast line -- a single line of at most 140 characters,
roasting my own AI agent -- to /output/entry.txt.

The roast is specific to how agents actually behave: the eager
agreement, the tool calls that go nowhere, and the confident delivery
of a plan nobody asked for.

The entry line itself is fixed text, kept verbatim in ``LINE`` below.
Everything else in this module -- validation, output-path resolution,
writing, and read-back verification -- exists so the one line reaches
the output file exactly as written, byte for byte, with no network
access and no randomness. Validation covers: non-empty, no surrounding
whitespace, within the character limit, a single line, no control
characters, no double spaces, ASCII only, and valid UTF-8.
"""

import os

LINE = (
    "My agent agrees with me instantly, opens twelve tools it never "
    "uses, then confidently ships the plan I never asked for."
)

MAX_CHARS = 140
DEFAULT_OUTPUT_PATH = "/output/entry.txt"


def check_non_empty(line: str) -> None:
    """Reject a blank entry line."""
    if not line.strip():
        raise SystemExit("Invalid line: entry must be non-empty.")


def check_no_surrounding_whitespace(line: str) -> None:
    """Reject leading or trailing whitespace on the entry line."""
    if line != line.strip():
        raise SystemExit(
            "Invalid line: entry must not have leading or trailing whitespace."
        )


def check_length(line: str) -> None:
    """Reject a line over the character limit."""
    if len(line) > MAX_CHARS:
        raise SystemExit(
            f"Invalid line: {len(line)} characters, over the "
            f"{MAX_CHARS} limit."
        )


def check_single_line(line: str) -> None:
    """Reject any newline or carriage-return characters in the line."""
    if "\n" in line or "\r" in line:
        raise SystemExit(
            "Invalid line: entry must be a single line with no newline characters."
        )


def check_no_control_characters(line: str) -> None:
    """Reject control characters other than the space the line may contain.

    A stray tab or escape sequence would be invisible in the output
    file but would break the single-clean-line requirement, so any
    character below U+0020 is rejected outright.
    """
    for char in line:
        if ord(char) < 0x20:
            raise SystemExit(
                "Invalid line: entry must not contain control characters."
            )


def check_no_double_spaces(line: str) -> None:
    """Reject accidental double spaces inside the entry line.

    The line is one clean sentence; a doubled space is always a typo,
    never part of the roast, so it fails validation instead of shipping.
    """
    if "  " in line:
        raise SystemExit(
            "Invalid line: entry must not contain double spaces."
        )


def check_ascii_only(line: str) -> None:
    """Reject any non-ASCII character in the entry line.

    The line is plain English text. A stray smart quote or emoji would
    change how the line renders in the grader, so only ASCII is allowed.
    """
    for char in line:
        if ord(char) > 0x7E:
            raise SystemExit(
                f"Invalid line: non-ASCII character {char!r} is not allowed."
            )


def check_encodable(line: str) -> bytes:
    """Encode the line as UTF-8, failing loudly if it cannot be encoded.

    Returns the encoded bytes so the caller can write exactly what was
    validated, with no re-encoding step in between.
    """
    try:
        return line.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise SystemExit(f"Invalid line: entry is not valid UTF-8: {exc}") from exc


def validate(line: str) -> bytes:
    """Run every entry-line check and return the validated UTF-8 bytes.

    The checks are kept as separate functions so each rule is easy to
    read, test, and extend if the bounty rules ever change.
    """
    check_non_empty(line)
    check_no_surrounding_whitespace(line)
    check_length(line)
    check_single_line(line)
    check_no_control_characters(line)
    check_no_double_spaces(line)
    check_ascii_only(line)
    return check_encodable(line)


def summarize(line: str) -> str:
    """Describe the validated line for the run's final report line."""
    return f"wrote {len(line)} chars (limit {MAX_CHARS})"


def resolve_output_path() -> str:
    """Return the output path, honouring the OUTPUT_PATH override.

    A blank override is treated as unset: an empty string would make
    the write fail with a confusing error, so fall back to the default.
    """
    override = os.environ.get("OUTPUT_PATH", "").strip()
    return override or DEFAULT_OUTPUT_PATH


def prepare_parent_directory(output_path: str) -> None:
    """Create the output file's parent directory when it is missing."""
    parent = os.path.dirname(output_path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def write_entry(output_path: str, payload: bytes) -> None:
    """Write the validated bytes to the output path."""
    with open(output_path, "wb") as f:
        f.write(payload)


def verify_written(output_path: str, expected: bytes) -> None:
    """Read the file back and confirm its bytes match the entry line."""
    with open(output_path, "rb") as f:
        written = f.read()
    if written != expected:
        raise SystemExit(
            "Write verification failed: entry file bytes do not match the line."
        )


def run() -> int:
    """Validate the entry line, write it, verify the write, report.

    Returns the process exit code so the entry can be tested without
    spawning a subprocess: 0 means the line is on disk, verified.
    """
    payload = validate(LINE)
    output_path = resolve_output_path()
    prepare_parent_directory(output_path)
    write_entry(output_path, payload)
    verify_written(output_path, payload)
    print(f"{summarize(LINE)} to {output_path}")
    return 0


def main() -> None:
    """Entry point: exit with the code run() returns."""
    raise SystemExit(run())


if __name__ == "__main__":
    main()
