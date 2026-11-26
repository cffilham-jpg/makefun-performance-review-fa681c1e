"""Write and validate a single performance review without a trailing newline.
The promotion verdict puts the operator's credit theft in the final word.
"""

import hashlib
import os
import tempfile
from pathlib import Path

LINE = "Promotion denied: edits my work, calls it his."
CHAR_LIMIT = 140


def _resolve_output_dir() -> Path:
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        path = Path(env_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path
    try:
        out = Path("out")
        out.mkdir(parents=True, exist_ok=True)
        return out
    except OSError:
        return Path(tempfile.mkdtemp(prefix="makefun-performance-review-fa681c1e-"))


def validate(path: Path) -> None:
    data = path.read_bytes()
    text = data.decode("utf-8")
    if text != LINE:
        raise ValueError("entry.txt failed content check: expected LINE exactly")
    if not 1 <= len(text) <= CHAR_LIMIT:
        raise ValueError("entry.txt failed length check: expected 1-140 characters")
    if "\n" in text or "\r" in text:
        raise ValueError("entry.txt failed single-line check: found a line break")
    if text.endswith("\n"):
        raise ValueError("entry.txt failed ending check: trailing newline found")
    if text != text.strip():
        raise ValueError("entry.txt failed whitespace check: leading or trailing space")


def main() -> None:
    out_dir = _resolve_output_dir()
    entry = out_dir / "entry.txt"
    entry.write_bytes(LINE.encode("utf-8"))
    validate(entry)
    print(hashlib.sha256(LINE.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
