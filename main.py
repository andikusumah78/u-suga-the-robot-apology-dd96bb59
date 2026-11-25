#!/usr/bin/env python3
"""The Robot Apology - make.fun entry.

Writes a two-line robot apology to /output/entry.txt.

The gate requires UTF-8 text of 1 to 400 characters, not only
whitespace, and the brief requires exactly two lines: one sentence
owning a specific mistake, one sentence naming the lesson that
follows from it. check_text() enforces both before anything is
written, and write_entry() reads the file back to prove the bytes
on disk are exactly the validated text.
"""

import os
import sys

# The apology, fixed: line 1 owns one concrete mistake, line 2
# names the lesson that follows from that exact mistake.
ENTRY_LINES = (
    "I am sorry I ironed your passport \u2014 the creases looked "
    "untidy, and I thought I was helping.",
    "I have learned that some wrinkles are load-bearing, so from "
    "now on I will ask before I press anything that has a "
    "photograph in it.",
)

GATE_MIN_CHARS = 1
GATE_MAX_CHARS = 400


def join_lines(lines):
    """Join the apology lines with one newline, no trailing newline."""
    return "\n".join(lines)


def check_text(text):
    """Check the text against the gate: 1-400 chars, not blank, UTF-8,
    and exactly two lines, as the brief requires."""
    if not isinstance(text, str):
        raise TypeError("entry text must be str")
    if not text.strip():
        raise ValueError("entry text must not be only whitespace")
    if len(text) < GATE_MIN_CHARS:
        raise ValueError("entry text is empty")
    if len(text) > GATE_MAX_CHARS:
        raise ValueError(
            "entry text is %d chars, over the %d limit"
            % (len(text), GATE_MAX_CHARS)
        )
    lines = text.split("\n")
    if len(lines) != 2:
        raise ValueError(
            "entry text must be exactly two lines, got %d" % len(lines)
        )
    if not all(line.strip() for line in lines):
        raise ValueError("each of the two lines must hold text")
    text.encode("utf-8")
    return text


def resolve_out_dir():
    """Return the output directory: MAKEFUN_OUTPUT_DIR, or "/output"."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def write_entry(text, out_dir):
    """Write text to entry.txt in out_dir and verify by reading it back."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    # Read back and verify: the file on disk must be exactly the
    # validated text, otherwise the run is not reproducible.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != text:
        raise ValueError(
            "read-back mismatch: entry.txt does not match the validated text"
        )
    return path


def main():
    text = check_text(join_lines(ENTRY_LINES))
    out_dir = resolve_out_dir()
    path = write_entry(text, out_dir)
    print("wrote %d chars to %s" % (len(text), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
