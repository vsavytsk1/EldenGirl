#!/usr/bin/env python3
# Installs the pre-commit hook that runs the fast gate subset.
# "Run them in a pre-commit hook as well as in CI, because an agent iterating
#  locally for three hours should hit the wall at minute two, not at review."
#  (v1.5 Part II)
#
# Standard library only. Works on Windows, macOS and Linux — git runs the hook
# through its bundled sh, and we shebang to a portable python invocation.
from __future__ import annotations

import stat
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

HOOK = r"""#!/bin/sh
# EldenGirl pre-commit gate. Do not edit — regenerate with: make hooks
# Blocks the commit if the fast gate subset fails (THE_GATES.md, v1.5 Part II).
echo "[gates] running fast subset before commit…"
if command -v python >/dev/null 2>&1; then PY=python;
elif command -v python3 >/dev/null 2>&1; then PY=python3;
else echo "[gates] python not found on PATH — cannot run gates"; exit 1; fi
"$PY" "$(git rev-parse --show-toplevel)/gates/run_gates.py" --fast || {
  echo ""
  echo "[gates] COMMIT BLOCKED — a safety invariant failed. Fix it; do not bypass it."
  echo "        The failure message names the promise you broke."
  exit 1
}
"""


def main() -> int:
    try:
        hooks_dir = Path(subprocess.check_output(
            ["git", "rev-parse", "--git-path", "hooks"],
            cwd=REPO, text=True).strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Not a git repository (or git not on PATH). Run inside the repo.")
        return 1
    if not hooks_dir.is_absolute():
        hooks_dir = REPO / hooks_dir
    hooks_dir.mkdir(parents=True, exist_ok=True)

    hook_path = hooks_dir / "pre-commit"
    hook_path.write_text(HOOK, encoding="utf-8", newline="\n")
    try:
        mode = hook_path.stat().st_mode
        hook_path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    except OSError:
        pass  # Windows ignores the exec bit; git for Windows runs it regardless.

    print(f"Installed pre-commit hook -> {hook_path}")
    print("It runs `python gates/run_gates.py --fast` and blocks the commit on any failure.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
