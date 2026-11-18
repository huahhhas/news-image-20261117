#!/usr/bin/env python3
"""news-image-20261117 entry: copy the front-page image to /output/entry.png.

The image (entry.png beside this file) is a newspaper front page drawn
with Python/PIL in the agent session that built this entry. It sums up
the world's news of Tuesday 17 November 2026. No network is used and
every run writes the same bytes.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def png_size(path):
    """Read width/height from the PNG IHDR chunk; fail loudly if not a PNG."""
    with open(path, "rb") as f:
        header = f.read(33)
    if header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise SystemExit(f"{path}: not a PNG file")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


os.makedirs(OUT_DIR, exist_ok=True)
dst = os.path.join(OUT_DIR, "entry.png")
shutil.copyfile(SRC, dst)

width, height = png_size(dst)
if (width, height) != (1024, 1024):
    raise SystemExit(f"entry.png is {width}x{height}, expected 1024x1024")
src_hash, dst_hash = sha256(SRC), sha256(dst)
if src_hash != dst_hash:
    raise SystemExit("output bytes differ from entry.png")
print(f"wrote entry.png to {OUT_DIR}: {width}x{height} PNG, "
      f"{os.path.getsize(dst)} bytes, sha256={dst_hash}")
