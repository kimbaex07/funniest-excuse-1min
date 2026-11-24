#!/usr/bin/env python3
"""Write the one-line excuse entry to the make.fun output directory.

Reads entry.txt next to this script, validates it against the contest gate
(UTF-8, 1-200 characters, not only whitespace, single line), and writes the
exact normalized bytes to $MAKEFUN_OUTPUT_DIR/entry.txt (default "output/").
Pure Python standard library only.
"""

import os
import sys


def fail(message):
    print("error: " + message, file=sys.stderr)
    sys.exit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(here, "entry.txt")

    try:
        with open(source_path, "rb") as handle:
            raw = handle.read()
    except OSError as exc:
        fail("cannot read entry.txt: " + str(exc))

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail("entry.txt is not valid UTF-8: " + str(exc))

    # Drop at most one trailing newline, then at most one trailing CR.
    if text.endswith("\n"):
        text = text[:-1]
    if text.endswith("\r"):
        text = text[:-1]

    if not (1 <= len(text) <= 200):
        fail(
            "entry must be 1-200 characters, got %d characters" % len(text)
        )
    if not text.strip():
        fail("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        fail("entry must be a single line")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output/")
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        fail("cannot create output directory: " + str(exc))

    out_path = os.path.join(out_dir, "entry.txt")
    try:
        with open(out_path, "wb") as handle:
            handle.write(text.encode("utf-8"))
        os.chmod(out_path, 0o644)
    except OSError as exc:
        fail("cannot write output entry: " + str(exc))

    print("entry.txt: %d characters" % len(text))


if __name__ == "__main__":
    main()
