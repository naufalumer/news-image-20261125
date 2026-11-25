#!/usr/bin/env python3
"""news-image-20261125: copy the pre-rendered front page to the output dir.

The image is drawn by render.py (kept out of this repo); this program only
copies the bundled entry.png to $MAKEFUN_OUTPUT_DIR/entry.png.
Stdlib only, no network, deterministic: the same bytes every run.
"""
import os
import shutil
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
MAX_BYTES = 1048576


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    if not os.path.isfile(SRC):
        print(f"entry.png missing next to {__file__}", file=sys.stderr)
        return 1
    if os.path.getsize(SRC) > MAX_BYTES:
        print(f"entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    with open(SRC, "rb") as fh:
        if fh.read(8) != b"\x89PNG\r\n\x1a\n":
            print("entry.png is not a PNG", file=sys.stderr)
            return 1
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    if os.path.getsize(dst) != os.path.getsize(SRC):
        print("copy size mismatch", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
