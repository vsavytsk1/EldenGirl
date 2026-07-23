#!/usr/bin/env python3
# ─────────────────────────────────────────────────────────────────────────────
# THE GATES — the safety invariants, executable.  (docs/THE_GATES.md, v1.5 Part II)
#
#   "Every gate fails the build. None of them warn.
#    A gate that warns is a comment."
#
# Task one, not task two. Runs in the pre-commit hook AND in CI so an agent
# iterating locally hits the wall in minute two, not at review.
#
#   python gates/run_gates.py            # full set
#   python gates/run_gates.py --fast     # the <5s subset, for the pre-commit hook
#   python gates/run_gates.py --artefact path/to/app-release.apk   # also scan a build
#
# Exit code is non-zero on ANY failure. Standard library only — this script is
# itself bound by S8 (no third-party SDKs) and must run on a bare Python 3.8+.
#
# WHAT RUNS NOW vs LATER
#   Source-level checks (G3-src, G6, G8, G9, G10, G11, G4-web) run always and fast.
#   Artefact-level checks (G1 merged manifest, G2 resolved graph, G3 binary strings,
#   G4 android zero-write, G5 FLAG_SECURE runtime, G7 backup config) run when their
#   target exists; otherwise they report SKIP — loudly, and never as a pass.
#
# SCOPING NOTE (important and deliberate):
#   G3 (forbidden lexicon) and G11 (cover identity) scan the DISGUISED tiers and
#   build config — android/, ios/, and gradle/build files. They do NOT scan:
#     - docs/       : the human-authored threat-model spec, which discusses the subject
#                     by necessity and is meant to be published (THE_APP.md Part VII).
#     - web/, lab/  : the codex/training ground/concept lab, PUBLIC by design — no
#                     disguise, handed over as a URL, holds no user data. Still bound
#                     by G4 zero-write, which DOES scan them.
#     - gates/      : these files literally define the forbidden terms and identity shapes.
#   The gate's job is to keep the subject and the chosen cover out of the DISGUISED
#   artefacts, not to censor the published specification.
# ─────────────────────────────────────────────────────────────────────────────
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GATES = REPO / "gates"

# Tiers that carry a disguise and therefore must say nothing.
DISGUISED_TIERS = ["android", "ios"]
# Public, zero-write reading tiers: the codex/training ground served to a browser.
# They are public BY DESIGN (no disguise, handed over as a URL, hold no user data),
# so they are exempt from the lexicon/identity scans but STILL bound by zero-write.
PUBLIC_WEB_TIERS = ["web", "lab"]
# Directories never scanned for lexicon / identity (see SCOPING NOTE above).
SCAN_EXCLUDE_DIRS = {".git", "docs", "web", "lab", "gates", "node_modules", "build",
                     ".gradle", "DerivedData", ".idea"}
SOURCE_EXTS = {".kt", ".kts", ".java", ".swift", ".xml", ".plist", ".gradle",
               ".properties", ".pro", ".m", ".h", ".mm", ".entitlements"}

# ── result plumbing ──────────────────────────────────────────────────────────
PASS, FAIL, SKIP = "PASS", "FAIL", "SKIP"


@dataclass
class Result:
    gate: str
    title: str
    status: str
    detail: str = ""
    findings: list[str] = field(default_factory=list)


def _supports_color() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("CI"):
        return True
    return sys.stdout.isatty()


_C = _supports_color()


def _col(s: str, code: str) -> str:
    return f"\033[{code}m{s}\033[0m" if _C else s


def _iter_source_files(roots: list[str]) -> list[Path]:
    out: list[Path] = []
    for root in roots:
        base = REPO / root
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_dir():
                continue
            if any(part in SCAN_EXCLUDE_DIRS for part in p.parts):
                continue
            if p.suffix in SOURCE_EXTS:
                out.append(p)
    return out


def _tracked_files() -> list[Path]:
    """All files under the repo except excluded dirs. Used by G11."""
    out: list[Path] = []
    for p in REPO.rglob("*"):
        if p.is_dir():
            continue
        parts = set(p.relative_to(REPO).parts)
        if parts & {".git", "node_modules", "build", ".gradle", "DerivedData"}:
            continue
        out.append(p)
    return out


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


# Build-only file types that NEVER enter the shipped artefact, so their contents
# cannot leak into the binary a phone can be searched for (G3 scans the artefact,
# never the build). Gradle/ProGuard/properties are compile-time only.
_BUILD_ONLY_EXTS = {".gradle", ".kts", ".properties", ".pro", ".cfg"}

_LINE_COMMENT = re.compile(r"//[^\n]*")
_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
_XML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def _strip_comments(text: str, suffix: str) -> str:
    """Remove comments so a source pre-check models what actually SHIPS.
    Comments are stripped by every compiler and never reach the artefact, so a
    forbidden term in a comment is not a binary leak. Identifiers and string
    literals survive and are still scanned."""
    if suffix in {".xml", ".plist", ".entitlements"}:
        return _XML_COMMENT.sub(" ", text)
    if suffix in {".kt", ".java", ".swift", ".m", ".h", ".mm"}:
        return _BLOCK_COMMENT.sub(" ", _LINE_COMMENT.sub(" ", text))
    return text


def _load_terms(name: str) -> list[str]:
    f = GATES / name
    if not f.exists():
        return []
    terms = []
    for line in _read(f).splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            terms.append(line)
    return terms


def _rel(p: Path) -> str:
    try:
        return str(p.relative_to(REPO)).replace("\\", "/")
    except ValueError:
        return str(p)


# ── G1 · ZERO PERMISSIONS IN THE MERGED MANIFEST ─────────────────────────────
def g1_permissions(artefact: Path | None) -> Result:
    title = "Zero permissions in the merged manifest"
    trace = "S8, S9, v1.3 Part II"
    android = REPO / "android"
    manifests = list(android.rglob("AndroidManifest.xml")) if android.exists() else []
    if not manifests:
        return Result("G1", title, SKIP,
                      "no AndroidManifest.xml yet — check the MERGED artefact once android/ builds")

    findings: list[str] = []
    # The defensive removals that must be present so a merge cannot inject them back.
    required_removed = {
        "android.permission.INTERNET",
        "android.permission.ACCESS_NETWORK_STATE",
        "android.permission.ACCESS_FINE_LOCATION",
        "android.permission.ACCESS_COARSE_LOCATION",
    }
    add_re = re.compile(r'<uses-permission[^>]*android:name="([^"]+)"[^>]*/?>')
    for m in manifests:
        text = _read(m)
        present_removed = set()
        for match in re.finditer(
                r'<uses-permission[^>]*android:name="([^"]+)"[^>]*tools:node="remove"',
                text):
            present_removed.add(match.group(1))
        # Any uses-permission that is NOT a tools:node="remove" is an additive grant.
        for match in add_re.finditer(text):
            name = match.group(1)
            block = text[match.start():match.end()]
            if 'tools:node="remove"' not in block:
                findings.append(f"{_rel(m)}: additive permission <{name}>")
        missing = required_removed - present_removed
        for name in sorted(missing):
            findings.append(f"{_rel(m)}: missing defensive removal for {name}")

    if findings:
        return Result("G1", title, FAIL,
                      f"[{trace}] the merged manifest must grant nothing; keep the "
                      f"tools:node=\"remove\" block intact", findings)
    return Result("G1", title, PASS,
                  "defensive removals present, no additive permissions in source "
                  "(still verify the MERGED artefact in CI)")


# ── G2 · DEPENDENCY ALLOWLIST, TRANSITIVE ────────────────────────────────────
def g2_deps(artefact: Path | None) -> Result:
    title = "Dependency allowlist (transitive)"
    trace = "S8 — no third-party SDKs"
    allow = set(_load_terms("allowed-deps.txt"))
    gradle_files = []
    for root in ["android"]:
        base = REPO / root
        if base.exists():
            gradle_files += list(base.rglob("build.gradle")) + list(base.rglob("build.gradle.kts"))
    if not gradle_files:
        return Result("G2", title, SKIP,
                      "no gradle module yet — full transitive check runs against the "
                      "resolved release classpath once android/ builds")

    # Source-level: every declared coordinate must be on the allowlist.
    coord_re = re.compile(r'["\']([a-z0-9.\-]+:[a-z0-9.\-]+:[^"\']+)["\']')
    findings = []
    for gf in gradle_files:
        for m in coord_re.finditer(_read(gf)):
            coord = m.group(1)
            if coord not in allow:
                findings.append(f"{_rel(gf)}: {coord} not in gates/allowed-deps.txt")
    if findings:
        return Result("G2", title, FAIL,
                      f"[{trace}] adding a coordinate is a human decision with a reason "
                      f"in the commit message", findings)
    return Result("G2", title, PASS,
                  "no declared dependency outside the allowlist "
                  "(verify transitively via ./gradlew dependencies in CI)")


# ── G3 · THE STRING TABLE SAYS NOTHING ───────────────────────────────────────
def g3_lexicon(artefact: Path | None) -> Result:
    title = "String table says nothing (forbidden lexicon)"
    trace = "v1.2 D3"
    terms = _load_terms("forbidden-lexicon.txt")
    if not terms:
        return Result("G3", title, FAIL,
                      f"[{trace}] gates/forbidden-lexicon.txt is empty — the gate cannot protect nothing")

    lowered = [(t, t.lower()) for t in terms]
    findings = []
    files = _iter_source_files(DISGUISED_TIERS)
    for p in files:
        # Build-only files (gradle/proguard/properties) never enter the artefact.
        if p.suffix in _BUILD_ONLY_EXTS:
            continue
        # Model what SHIPS: strip comments (compilers do), keep identifiers and
        # string literals. Class/method-name leaks like DecoyManager still fail.
        text = _strip_comments(_read(p), p.suffix).lower()
        for original, term in lowered:
            if term in text:
                findings.append(f"{_rel(p)}: contains \"{original}\" (source pre-check; "
                                f"authoritative check is --artefact against the release binary)")

    # Artefact scan: strings of the release binary, if one was provided.
    scanned_artefact = False
    if artefact and artefact.exists():
        scanned_artefact = True
        blob = artefact.read_bytes()
        found_strings = _extract_strings(blob)
        hay = "\n".join(found_strings).lower()
        for original, term in lowered:
            if term in hay:
                findings.append(f"{_rel(artefact)} (binary): contains \"{original}\"")

    if findings:
        return Result("G3", title, FAIL,
                      f"[{trace}] the content payload is encrypted and decrypted in memory; "
                      f"no subject-matter string may appear in a disguised tier", findings)
    note = "scanned android/ + ios/ source"
    note += " + release artefact" if scanned_artefact else " (no artefact given — scan the release binary in CI)"
    return Result("G3", title, PASS, note)


def _extract_strings(blob: bytes, minlen: int = 4) -> list[str]:
    out, cur = [], bytearray()
    for b in blob:
        if 32 <= b < 127:
            cur.append(b)
        else:
            if len(cur) >= minlen:
                out.append(cur.decode("ascii", "ignore"))
            cur = bytearray()
    if len(cur) >= minlen:
        out.append(cur.decode("ascii", "ignore"))
    return out


# ── G4 · ZERO WRITES (web tiers static form; android is an instrumented test) ─
def g4_zero_write(artefact: Path | None) -> Result:
    title = "Zero writes"
    trace = "v1.4 Part III"
    roots = [REPO / t for t in PUBLIC_WEB_TIERS if (REPO / t).exists()]
    if not roots:
        return Result("G4", title, SKIP, "no web/ or lab/ tier present")

    findings = []
    # Static: no persistence API may appear in any shipped HTML/JS.
    storage_re = re.compile(
        r"\b(localStorage|sessionStorage|indexedDB|openDatabase|document\.cookie|"
        r"navigator\.storage|caches\.open|serviceWorker\.register|new\s+Worker)\b")
    net_re = re.compile(r"\b(fetch\s*\(|XMLHttpRequest|navigator\.sendBeacon|WebSocket|EventSource)\b")
    scanned = 0
    for root in roots:
        # A manifest or service worker makes the browser want to INSTALL the page — banned.
        for bad in list(root.rglob("manifest.json")) + list(root.rglob("*serviceworker*")) \
                + list(root.rglob("sw.js")) + list(root.rglob("service-worker.js")):
            findings.append(f"{_rel(bad)}: must not be installable (no manifest / service worker)")
        for p in list(root.rglob("*.html")) + list(root.rglob("*.js")):
            scanned += 1
            text = _read(p)
            for m in storage_re.finditer(text):
                findings.append(f"{_rel(p)}: persistence API '{m.group(1)}' (must write 0 bytes)")
            for m in net_re.finditer(text):
                findings.append(f"{_rel(p)}: network call '{m.group(1)}' (must work fully offline, S8)")

    if findings:
        return Result("G4", title, FAIL,
                      f"[{trace}] one hour of use must change zero bytes; the public web "
                      f"tiers store nothing and call nothing", findings)
    tiers = " + ".join(f"{t}/" for t in PUBLIC_WEB_TIERS if (REPO / t).exists())
    return Result("G4", title, PASS,
                  f"{tiers} use no storage or network API and are not installable "
                  f"({scanned} file(s); android sandbox zero-write is an instrumented test — G4)")


# ── G5 · FLAG_SECURE EVERYWHERE ──────────────────────────────────────────────
def g5_flag_secure(artefact: Path | None) -> Result:
    title = "FLAG_SECURE everywhere"
    trace = "S7"
    android = REPO / "android"
    kt = _iter_source_files(["android"]) if android.exists() else []
    if not kt:
        return Result("G5", title, SKIP,
                      "no android/ source yet — set FLAG_SECURE centrally in "
                      "ActivityLifecycleCallbacks and assert per-Activity in an instrumented test")
    findings = []
    for p in kt:
        text = _read(p)
        for m in re.finditer(r"clearFlags\s*\([^)]*FLAG_SECURE", text):
            findings.append(f"{_rel(p)}: clears FLAG_SECURE")
    has_set = any("FLAG_SECURE" in _read(p) and "clearFlags" not in _read(p) for p in kt)
    if findings:
        return Result("G5", title, FAIL,
                      f"[{trace}] FLAG_SECURE must never be cleared", findings)
    if not has_set:
        return Result("G5", title, FAIL,
                      f"[{trace}] android/ source sets FLAG_SECURE nowhere — set it centrally "
                      "so a new Activity cannot miss it")
    return Result("G5", title, PASS, "FLAG_SECURE set and never cleared in source")


# ── G6 · SILENT IN RELEASE ───────────────────────────────────────────────────
def g6_silent(artefact: Path | None) -> Result:
    title = "Silent in release (no logging, no mapping file)"
    trace = "S8"
    log_re = re.compile(r"\b(Log\.[vdiwe]|println|System\.out|NSLog|os_log|print)\s*\(")
    findings = []
    for p in _iter_source_files(DISGUISED_TIERS):
        for m in log_re.finditer(_read(p)):
            findings.append(f"{_rel(p)}: logging call '{m.group(1)}('")
    # A committed R8/ProGuard mapping is a de-obfuscation key.
    for mp in REPO.rglob("mapping.txt"):
        if ".git" not in mp.parts:
            findings.append(f"{_rel(mp)}: mapping file must never be committed or shipped")
    if findings:
        return Result("G6", title, FAIL,
                      f"[{trace}] release builds emit nothing and ship no mapping file", findings)
    return Result("G6", title, PASS, "no logging calls in disguised tiers, no committed mapping file")


# ── G7 · BACKUP AND DEVICE-TRANSFER EXCLUSION ────────────────────────────────
def g7_backup(artefact: Path | None) -> Result:
    title = "Backup AND device-transfer exclusion"
    trace = "S4, v1.5 Part III·5"
    android = REPO / "android"
    manifests = list(android.rglob("AndroidManifest.xml")) if android.exists() else []
    if not manifests:
        return Result("G7", title, SKIP,
                      "no AndroidManifest.xml yet — needs allowBackup=false + a "
                      "data_extraction_rules.xml excluding both cloud-backup and device-transfer")
    findings = []
    for m in manifests:
        text = _read(m)
        if 'android:allowBackup="false"' not in text:
            findings.append(f"{_rel(m)}: android:allowBackup must be \"false\"")
        if "dataExtractionRules" not in text:
            findings.append(f"{_rel(m)}: android:dataExtractionRules not set (API 31 split)")
    rules = list(android.rglob("data_extraction_rules.xml"))
    if not rules:
        findings.append("res/xml/data_extraction_rules.xml missing")
    for r in rules:
        text = _read(r)
        if "<cloud-backup" not in text:
            findings.append(f"{_rel(r)}: no <cloud-backup> exclusions")
        if "<device-transfer" not in text:
            findings.append(f"{_rel(r)}: no <device-transfer> exclusions")
    if findings:
        return Result("G7", title, FAIL,
                      f"[{trace}] both cloud backup and device-to-device transfer must "
                      f"exclude every domain", findings)
    return Result("G7", title, PASS, "allowBackup=false and both transfer paths excluded")


# ── G8 · KEYS STAY ON THE DEVICE, NO BIOMETRICS ──────────────────────────────
def g8_keys(artefact: Path | None) -> Result:
    title = "Keys stay on the device; biometrics banned"
    trace = "S4, Adversary B, v1.2 Part II, v1.4 Part VI"
    findings = []
    src = _iter_source_files(DISGUISED_TIERS)
    bio_re = re.compile(r"\b(BiometricPrompt|FaceID|TouchID|LocalAuthentication|LAContext|"
                        r"setUserAuthenticationRequired\s*\(\s*true)\b")
    for p in src:
        text = _read(p)
        for m in bio_re.finditer(text):
            findings.append(f"{_rel(p)}: biometric/auth API '{m.group(1)}' (compellable — banned)")
        # iOS keychain must be ThisDeviceOnly and not synchronizable.
        for m in re.finditer(r"kSecAttrSynchronizable\s*[:=].*", text):
            if "kCFBooleanFalse" not in m.group(0) and "false" not in m.group(0).lower():
                findings.append(f"{_rel(p)}: kSecAttrSynchronizable not pinned false (iCloud Keychain)")
        for m in re.finditer(r"kSecAttrAccessible\w*", text):
            if "WhenUnlockedThisDeviceOnly" not in m.group(0):
                findings.append(f"{_rel(p)}: {m.group(0)} — must be ...WhenUnlockedThisDeviceOnly")
    if findings:
        return Result("G8", title, FAIL,
                      f"[{trace}] the key never leaves the device and biometrics are not a preference",
                      findings)
    if not src:
        return Result("G8", title, SKIP, "no android/ or ios/ source yet")
    return Result("G8", title, PASS, "no biometric APIs; keychain attributes device-only in source")


# ── G9 · NO TEXT FIELD LEARNS ────────────────────────────────────────────────
def g9_text_fields(artefact: Path | None) -> Result:
    title = "No text field learns"
    trace = "v1.5 Part III·1 — the keyboard"
    src = _iter_source_files(DISGUISED_TIERS)
    if not src:
        return Result("G9", title, SKIP,
                      "no record-tier source yet — the ONLY permitted text input is a single "
                      "wrapper with the no-learning flags baked in")
    # Any raw text-input widget outside the one sanctioned wrapper is a finding.
    raw_re = re.compile(r"\b(TextField|OutlinedTextField|EditText|UITextView|UITextField)\b")
    wrapper_markers = ("NoLearnField", "SafeTextField", "PrivateField")  # the sanctioned wrapper name(s)
    clip_re = re.compile(r"\b(ClipboardManager|UIPasteboard|LocalClipboardManager|setPrimaryClip)\b")
    findings = []
    for p in src:
        text = _read(p)
        # Allow the wrapper's own definition file to reference the raw widget once.
        is_wrapper = any(w in text for w in wrapper_markers)
        for m in raw_re.finditer(text):
            if not is_wrapper:
                findings.append(f"{_rel(p)}: raw '{m.group(1)}' — use the no-learning wrapper only")
        for m in clip_re.finditer(text):
            findings.append(f"{_rel(p)}: clipboard use '{m.group(1)}' (readable by overlay access)")
    if findings:
        return Result("G9", title, FAIL,
                      f"[{trace}] the IME is a logging device that ships with the phone", findings)
    return Result("G9", title, PASS, "no raw text fields or clipboard use outside the wrapper")


# ── G10 · NO ART ─────────────────────────────────────────────────────────────
def g10_no_art(artefact: Path | None) -> Result:
    title = "No art (only the generated launcher icon)"
    trace = "v1.3 Part II"
    android = REPO / "android"
    if not android.exists():
        return Result("G10", title, SKIP, "no android/ res yet")
    findings = []
    for p in android.rglob("*"):
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
            rel = _rel(p)
            # Launcher icons are the sole exception AND must be generated, not committed.
            if "mipmap" in rel and "ic_launcher" in p.name:
                findings.append(f"{rel}: launcher bitmap committed — must be GENERATED from COVER_ICON_SEED")
            else:
                findings.append(f"{rel}: bitmap asset (draw with Canvas — nothing to reverse-engineer)")
    if findings:
        return Result("G10", title, FAIL,
                      f"[{trace}] zero bitmaps; the launcher icon is generated at build time", findings)
    return Result("G10", title, PASS, "no committed bitmaps")


# ── G11 · THE COVER IDENTITY IS NOT IN THE REPO ──────────────────────────────
def g11_cover_identity(artefact: Path | None) -> Result:
    title = "Cover identity is not in the repo"
    trace = "v1.5 Part I"
    patterns_raw = _load_terms("reserved-identity-patterns.txt")
    findings = []
    compiled = []
    for pat in patterns_raw:
        try:
            compiled.append((pat, re.compile(pat, re.IGNORECASE)))
        except re.error as e:
            findings.append(f"gates/reserved-identity-patterns.txt: bad regex {pat!r}: {e}")

    identity_file = GATES / "reserved-identity-patterns.txt"
    for p in _tracked_files():
        # Never scan the pattern-definition file itself, the docs (the published
        # spec), or the web codex (public by design). See SCOPING NOTE at top.
        rel_parts = set(p.relative_to(REPO).parts)
        if p == identity_file or (rel_parts & {"docs", "web", "gates"}):
            continue
        if p.suffix.lower() not in (SOURCE_EXTS | {".md", ".json", ".yml", ".yaml", ".txt", ".cfg"}):
            continue
        text = _read(p)
        for pat, rx in compiled:
            for m in rx.finditer(text):
                snippet = m.group(0).strip()[:80]
                findings.append(f"{_rel(p)}: matches reserved-identity pattern -> {snippet!r}")

    # The placeholders must still be placeholders.
    gp = REPO / "gradle.properties"
    if gp.exists():
        gtext = _read(gp)
        if not re.search(r"^\s*COVER_NAME\s*=\s*PLACEHOLDER\s*$", gtext, re.MULTILINE):
            findings.append("gradle.properties: COVER_NAME must stay = PLACEHOLDER")
        if not re.search(r"^\s*COVER_PACKAGE\s*=\s*org\.placeholder\.app\s*$", gtext, re.MULTILINE):
            findings.append("gradle.properties: COVER_PACKAGE must stay = org.placeholder.app")

    # Signing material and cover screenshots must not exist at all.
    for p in _tracked_files():
        low = p.name.lower()
        if any(low.endswith(ext) for ext in
               (".keystore", ".jks", ".p12", ".pfx", ".mobileprovision")):
            findings.append(f"{_rel(p)}: signing material must never be committed")

    if findings:
        return Result("G11", title, FAIL,
                      f"[{trace}] the disguise is defeated by a search engine — no real cover "
                      f"name, package, domain or key in any tracked file", findings)
    return Result("G11", title, PASS,
                  "placeholders intact, no reserved-identity match, no signing material")


# ── runner ───────────────────────────────────────────────────────────────────
# (gate fn, is_fast) — "fast" gates form the <5s pre-commit subset.
ALL_GATES = [
    (g1_permissions, False),
    (g2_deps, False),
    (g3_lexicon, True),
    (g4_zero_write, True),
    (g5_flag_secure, True),
    (g6_silent, True),
    (g7_backup, False),
    (g8_keys, True),
    (g9_text_fields, True),
    (g10_no_art, True),
    (g11_cover_identity, True),
]


def main() -> int:
    ap = argparse.ArgumentParser(description="Run THE GATES (docs/THE_GATES.md).")
    ap.add_argument("--fast", action="store_true",
                    help="run only the <5s subset (for the pre-commit hook)")
    ap.add_argument("--artefact", type=Path, default=None,
                    help="path to a release artefact (apk/app binary) to also scan")
    args = ap.parse_args()

    artefact = args.artefact if args.artefact and args.artefact.exists() else None
    if args.artefact and not artefact:
        print(_col(f"! artefact not found: {args.artefact}", "33"))

    gates = [(fn, fast) for (fn, fast) in ALL_GATES if (fast or not args.fast)]

    print(_col("─" * 74, "90"))
    print(_col(f"  THE GATES  ·  {'fast subset' if args.fast else 'full set'}  ·  "
               "green means nothing broke, not that it works", "1"))
    print(_col("─" * 74, "90"))

    results = [fn(artefact) for (fn, _fast) in gates]

    n_fail = n_skip = n_pass = 0
    for r in results:
        if r.status == FAIL:
            tag, code, n_fail = "FAIL", "1;31", n_fail + 1
        elif r.status == SKIP:
            tag, code, n_skip = "SKIP", "33", n_skip + 1
        else:
            tag, code, n_pass = "PASS", "32", n_pass + 1
        print(f"  {_col(tag, code)}  {_col(r.gate, '1')}  {r.title}")
        if r.detail:
            print(_col(f"          {r.detail}", "90"))
        for f in r.findings[:40]:
            print(_col(f"          → {f}", "31"))
        if len(r.findings) > 40:
            print(_col(f"          → … and {len(r.findings) - 40} more", "31"))

    print(_col("─" * 74, "90"))
    summary = f"  {n_pass} passed · {n_skip} skipped · {n_fail} failed"
    print(_col(summary, "1;31" if n_fail else "1;32"))
    if n_skip:
        print(_col("  skipped gates have no artefact/module YET — they are not passes.", "33"))
    print(_col("─" * 74, "90"))

    return 1 if n_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
