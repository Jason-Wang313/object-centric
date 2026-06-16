"""Build the final v4 object-centric paper and copy it to Desktop."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PDF = ROOT / "paper" / "object_binding_tail_audit_iclr.pdf"
FINAL_DIR = ROOT / "paper" / "final"
FINAL_NAME = "object centric-v4.pdf"
FINAL_PDF = FINAL_DIR / FINAL_NAME
DESKTOP = Path.home() / "OneDrive" / "Desktop"
DESKTOP_PDF = DESKTOP / FINAL_NAME
OLD_DESKTOPS = [
    DESKTOP / "object centric-v3.pdf",
    DESKTOP / "object centric-v2.pdf",
]
SOURCE_MAP = DESKTOP / "PAPER_SOURCE_MAP.md"
MANIFEST = FINAL_DIR / "object_centric_v4_manifest.json"
MIN_PAGES = 25


def run(command: list[str]) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def page_count(path: Path) -> int:
    proc = subprocess.run(
        ["pdfinfo", str(path)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    for line in proc.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise RuntimeError(f"could not read page count from {path}")


def pdf_text(path: Path) -> str:
    text_path = ROOT / "build" / "v4_pdf_text.txt"
    text_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["pdftotext", "-layout", str(path), str(text_path)], cwd=ROOT, check=True)
    return text_path.read_text(encoding="utf-8", errors="replace")


def check_v4_text(path: Path) -> None:
    text = pdf_text(path)
    compact = "".join(ch for ch in text.lower() if ch.isalnum())
    required = [
        "objectslotsunderselectionpressure",
        "protocolfreeze",
        "iclrstylerubric",
        "v4reviewerattackledger",
        "benchmarkstylesynthetictasksuite",
        "deployablenoleak",
        "supportcovered",
        "slotattention",
        "conformalprediction",
    ]
    missing = [term for term in required if term not in compact]
    if missing:
        raise RuntimeError(f"v4 PDF text is missing required terms: {missing}")
    forbidden = [
        "we validate on real robots",
        "we solve real robot planning",
        "we claim broad benchmark superiority",
        "achieves broad benchmark superiority",
        "state of the art",
        "is a universal repair",
        "guarantees recovery",
    ]
    hits = [term for term in forbidden if term in text.lower()]
    if hits:
        raise RuntimeError(f"v4 PDF text contains forbidden positive claims: {hits}")


def update_source_map() -> None:
    expected = f"| `{FINAL_NAME}` | `{ROOT}` | `Jason-Wang313/object-centric` |"
    if not SOURCE_MAP.exists():
        raise FileNotFoundError(SOURCE_MAP)
    text = SOURCE_MAP.read_text(encoding="utf-8")
    old_rows = [
        f"| `object centric-v3.pdf` | `{ROOT}` | `Jason-Wang313/object-centric` |",
        f"| `object centric-v2.pdf` | `{ROOT}` | `Jason-Wang313/object-centric` |",
    ]
    if expected not in text:
        replaced = False
        for old in old_rows:
            if old in text:
                text = text.replace(old, expected)
                replaced = True
        if not replaced:
            text = text.rstrip() + "\n" + expected + "\n"
    SOURCE_MAP.write_text(text, encoding="utf-8")


def main() -> int:
    run([sys.executable, "experiments/v4_cached_evidence.py"])
    run(["bash", "scripts/build_iclr_paper.sh"])
    if not SOURCE_PDF.exists():
        raise FileNotFoundError(SOURCE_PDF)

    check_v4_text(SOURCE_PDF)
    pages = page_count(SOURCE_PDF)
    if pages < MIN_PAGES:
        raise RuntimeError(f"v4 paper has {pages} pages, below required {MIN_PAGES}")

    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE_PDF, FINAL_PDF)
    DESKTOP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(FINAL_PDF, DESKTOP_PDF)
    for old_desktop in OLD_DESKTOPS:
        if old_desktop.exists():
            old_desktop.unlink()
    update_source_map()

    repo_sha = sha256(FINAL_PDF)
    desktop_sha = sha256(DESKTOP_PDF)
    if repo_sha != desktop_sha:
        raise RuntimeError("repo and Desktop final PDFs differ")

    payload = {
        "paper": "object centric",
        "version": "v4",
        "pages": pages,
        "min_pages": MIN_PAGES,
        "source_pdf": str(SOURCE_PDF),
        "repo_final_pdf": str(FINAL_PDF),
        "desktop_pdf": str(DESKTOP_PDF),
        "sha256": repo_sha,
        "old_desktop_pdfs_removed": all(not item.exists() for item in OLD_DESKTOPS),
        "uses_cached_v4_evidence": True,
        "generated_evidence": "results/v4_cached_evidence_summary.json",
    }
    MANIFEST.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
