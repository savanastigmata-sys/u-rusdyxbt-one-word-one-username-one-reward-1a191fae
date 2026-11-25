"""One Word, One Username, One Reward — entry program.

Writes the entrant's own make.fun username, one word and nothing else,
to ``entry.txt`` inside the output directory.

Rules enforced (see the competition gate):
  * the text is UTF-8, 1 to 30 characters, not only white space;
  * it is a single word: no spaces, no padding, no extra gloss.

The username is a plain constant: the program is fully deterministic,
uses only the Python standard library, and performs no network access.
"""

import os
import sys

# The entrant's own make.fun username, sent as one word and nothing else.
USERNAME = "savana"

MAX_CHARS = 30


def resolve_output_dir():
    """Return the output directory.

    The grader sets MAKEFUN_OUTPUT_DIR; without it, fall back to a local
    ``./output`` directory so the program still runs standalone.
    """
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out:
        return out
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "output")


def validate(text):
    """Enforce the competition gate on the entry text.

    Raises ValueError on any violation; returns the text unchanged.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(
            "entry must be 1 to 30 characters, got %d" % len(text)
        )
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing padding")
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if any(ch.isspace() for ch in text):
        raise ValueError("entry must be a single word with no spaces")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry must not contain control characters")
    text.encode("utf-8")  # must be valid UTF-8 text
    return text


def main():
    text = validate(USERNAME)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    # Read back and prove the file on disk is exactly the validated text.
    with open(path, "r", encoding="utf-8", newline="") as fh:
        written = fh.read()
    if written != text:
        raise ValueError("entry.txt on disk does not match validated text")
    return 0


if __name__ == "__main__":
    sys.exit(main())
