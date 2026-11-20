#!/usr/bin/env python3
"""Entry point for the news-image-20261120 competition.

Copies the entry image (entry.png, sitting beside this file in the
repository) into the output directory and verifies the copy byte for
byte by comparing SHA-256 digests, so a truncated or corrupted write
is caught instead of silently submitted.

Standard library only; no network. The output directory is taken
from MAKEFUN_OUTPUT_DIR, defaulting to /output.
"""
import hashlib
import os
import shutil
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")

    shutil.copyfile(SOURCE, dest)

    source_hash = sha256_of(SOURCE)
    dest_hash = sha256_of(dest)
    if source_hash != dest_hash:
        print(f"error: copy mismatch: {SOURCE} {source_hash} != "
              f"{dest} {dest_hash}", file=sys.stderr)
        return 1

    size = os.path.getsize(dest)
    print(f"wrote {dest} ({size} bytes, sha256 {dest_hash})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
