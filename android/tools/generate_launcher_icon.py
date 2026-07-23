#!/usr/bin/env python3
# ─────────────────────────────────────────────────────────────────────────────
# G10 · The launcher icon is the SOLE permitted bitmap, and it is GENERATED at
# build time from COVER_ICON_SEED — never committed. A committed launcher PNG
# fails the gate (v1.3 Part II).
#
# This generator is deterministic given the seed, so the build stays reproducible
# (THE_APP.md Part III) and the distributing organisation can publish the seed
# alongside the hash. It writes the mipmap PNGs into app/src/main/res/ at build
# time; those output paths are git-ignored.
#
# Standard-library only (S8 applies to our tooling). It draws a plain, neutral
# glyph — the REAL cover's icon design is chosen by the distributor and is not in
# this repo (v1.5 Part I). This default is a featureless placeholder tile.
#
#   python android/tools/generate_launcher_icon.py --seed <COVER_ICON_SEED>
# ─────────────────────────────────────────────────────────────────────────────
from __future__ import annotations

import argparse
import hashlib
import struct
import zlib
from pathlib import Path

# Android launcher densities.
DENSITIES = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
RES = Path(__file__).resolve().parent.parent / "app" / "src" / "main" / "res"


def _seed_color(seed: str) -> tuple[int, int, int]:
    h = hashlib.sha256(seed.encode("utf-8")).digest()
    # Muted, neutral tone — nothing eye-catching, nothing that reads as "special".
    r = 40 + h[0] % 40
    g = 40 + h[1] % 40
    b = 48 + h[2] % 40
    return r, g, b


def _png(width: int, height: int, rgb: tuple[int, int, int]) -> bytes:
    r, g, b = rgb
    raw = bytearray()
    for _ in range(height):
        raw.append(0)  # filter byte per scanline
        raw += bytes((r, g, b)) * width

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)  # 8-bit, RGB
    idat = zlib.compress(bytes(raw), 9)
    return sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", default="PLACEHOLDER",
                    help="COVER_ICON_SEED (the repo default is the placeholder)")
    args = ap.parse_args()

    rgb = _seed_color(args.seed)
    for name, size in DENSITIES.items():
        out_dir = RES / f"mipmap-{name}"
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "ic_launcher.png").write_bytes(_png(size, size, rgb))
    print(f"Generated launcher icons from seed (color rgb{rgb}). "
          f"These outputs are git-ignored (G10).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
