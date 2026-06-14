"""Build the final v3 object-centric paper and copy it to Desktop."""

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
FINAL_NAME = "object centric-v3.pdf"
FINAL_PDF = FINAL_DIR / FINAL_NAME
DESKTOP = Path.home() / "OneDrive" / "Desktop"
DESKTOP_PDF = DESKTOP / FINAL_NAME
OLD_DESKTOP_PDF = DESKTOP / "object centric-v2.pdf"
MANIFEST = FINAL_DIR / "object_centric_v3_manifest.json"
MIN_PAGES = 25


def run(command: list[str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def page_count(path: Path) -> int:
    try:
        proc = subprocess.run(
            ["pdfinfo", str(path)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        for line in proc.stdout.splitlines():
            if line.startswith("Pages:"):
                return int(line.split(":", 1)[1].strip())
    except (FileNotFoundError, subprocess.CalledProcessError, ValueError):
        pass
    data = path.read_bytes()
    return data.count(b"/Type /Page")


def main() -> int:
    run([sys.executable, "scripts/prepare_v3_evidence.py"])
    run(["bash", "scripts/build_iclr_paper.sh"])
    if not SOURCE_PDF.exists():
        raise FileNotFoundError(SOURCE_PDF)

    pages = page_count(SOURCE_PDF)
    if pages < MIN_PAGES:
        raise SystemExit(f"v3 paper has {pages} pages, below required {MIN_PAGES}")

    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE_PDF, FINAL_PDF)
    DESKTOP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(FINAL_PDF, DESKTOP_PDF)
    if OLD_DESKTOP_PDF.exists():
        OLD_DESKTOP_PDF.unlink()

    repo_sha = sha256(FINAL_PDF)
    desktop_sha = sha256(DESKTOP_PDF)
    if repo_sha != desktop_sha:
        raise SystemExit("repo and Desktop final PDFs differ")

    payload = {
        "paper": "object centric",
        "version": "v3",
        "pages": pages,
        "min_pages": MIN_PAGES,
        "source_pdf": str(SOURCE_PDF),
        "repo_final_pdf": str(FINAL_PDF),
        "desktop_pdf": str(DESKTOP_PDF),
        "sha256": repo_sha,
        "old_desktop_pdf_removed": not OLD_DESKTOP_PDF.exists(),
        "uses_cached_v3_evidence": True,
    }
    MANIFEST.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
