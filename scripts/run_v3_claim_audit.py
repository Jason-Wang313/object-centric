"""Strict v3 audit for the object-centric final paper artifact."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DESKTOP = Path.home() / "OneDrive" / "Desktop"
SOURCE_MAP = DESKTOP / "PAPER_SOURCE_MAP.md"
FINAL_NAME = "object centric-v3.pdf"
OLD_NAME = "object centric-v2.pdf"
REPO_FINAL = ROOT / "paper" / "final" / FINAL_NAME
DESKTOP_FINAL = DESKTOP / FINAL_NAME
MANIFEST = ROOT / "paper" / "final" / "object_centric_v3_manifest.json"
TEX = ROOT / "paper" / "object_binding_tail_audit_iclr.tex"
MIN_PAGES = 25


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
    return path.read_bytes().count(b"/Type /Page")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def fail(problems: list[str], message: str) -> None:
    problems.append(message)


def audit_text(problems: list[str]) -> None:
    text = TEX.read_text(encoding="utf-8")
    lowered = text.lower()
    required_terms = {
        "object": 80,
        "slot": 25,
        "identity": 25,
        "occlusion": 8,
        "hidden": 15,
        "merge/split": 5,
        "probe": 12,
        "support-covered": 8,
        "deployable no-leak": 8,
    }
    for term, minimum in required_terms.items():
        count = lowered.count(term)
        if count < minimum:
            fail(problems, f"object-centric term '{term}' appears {count} times, below {minimum}")
    forbidden_positive = [
        "validated on real robot",
        "real-robot evidence",
        "real robot evidence",
        "broad benchmark superiority",
        "state-of-the-art",
        "sota",
        "universal repair",
        "guaranteed recovery",
        "guarantees 100% recovery",
    ]
    safe_negators = ("no ", "not ", "unsupported", "does not", "do not", "without", "rather than", "not a")
    for lineno, line in enumerate(text.splitlines(), start=1):
        low = line.lower()
        for phrase in forbidden_positive:
            if phrase in low and not any(negator in low for negator in safe_negators):
                fail(problems, f"possible overclaim at tex line {lineno}: {line.strip()}")
    if "best-of" in lowered or "best of n" in lowered:
        fail(problems, "manuscript still contains best-of wording")
    required_sections = [
        "\\section{Introduction}",
        "\\section{A Selected-Utility Law for Object-Tail Audits}",
        "\\section{Controlled Object-Centric Candidate Populations}",
        "\\section{Repair Tiers and Leakage Control}",
        "\\section{Experimental Evidence}",
        "\\section{Self-Attack Summary}",
        "\\section{Limitations}",
        "\\section{Reproducibility}",
        "\\section{Conclusion}",
        "\\section{Fifty-Round Self-Attack Ledger}",
    ]
    for marker in required_sections:
        if marker not in text:
            fail(problems, f"missing manuscript section marker: {marker}")


def main() -> int:
    problems: list[str] = []

    for path in [REPO_FINAL, DESKTOP_FINAL, MANIFEST, TEX, SOURCE_MAP]:
        if not path.exists():
            fail(problems, f"missing required file: {path}")
    if problems:
        print(json.dumps({"passes": False, "problems": problems}, indent=2))
        return 1

    pages = page_count(REPO_FINAL)
    if pages < MIN_PAGES:
        fail(problems, f"repo final PDF has {pages} pages, below {MIN_PAGES}")
    desktop_pages = page_count(DESKTOP_FINAL)
    if desktop_pages != pages:
        fail(problems, f"Desktop page count {desktop_pages} does not match repo {pages}")

    repo_sha = sha256(REPO_FINAL)
    desktop_sha = sha256(DESKTOP_FINAL)
    if repo_sha != desktop_sha:
        fail(problems, "repo final PDF and Desktop PDF hashes differ")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("sha256") != repo_sha:
        fail(problems, "manifest sha256 does not match final PDF")
    if manifest.get("pages") != pages:
        fail(problems, "manifest page count does not match final PDF")
    if (DESKTOP / OLD_NAME).exists():
        fail(problems, f"old Desktop PDF still exists: {OLD_NAME}")

    source_map = SOURCE_MAP.read_text(encoding="utf-8")
    expected_row = f"| `{FINAL_NAME}` | `{ROOT}` | `Jason-Wang313/object-centric` |"
    if expected_row not in source_map:
        fail(problems, "PAPER_SOURCE_MAP.md does not contain the exact v3 object-centric row")
    if OLD_NAME in source_map:
        fail(problems, "PAPER_SOURCE_MAP.md still references object centric-v2.pdf")

    summary = json.loads((ROOT / "results" / "v3_object_centric_evidence_summary.json").read_text(encoding="utf-8"))
    if not summary.get("uses_cached_artifacts_only"):
        fail(problems, "v3 summary does not declare cached artifacts only")
    if not summary.get("passes_claim_audit"):
        fail(problems, "cached v3 summary says base claim audit did not pass")

    attack_rows = read_csv(ROOT / "results" / "tables" / "v3_object_centric_attack_ledger.csv")
    if len(attack_rows) != 50:
        fail(problems, f"attack ledger has {len(attack_rows)} rows, expected 50")
    allowed_attack_status = {"pass", "bounded"}
    bad_status = sorted({row.get("status", "") for row in attack_rows} - allowed_attack_status)
    if bad_status:
        fail(problems, f"attack ledger has bad statuses: {bad_status}")
    if sum(row.get("status") == "bounded" for row in attack_rows) < 3:
        fail(problems, "attack ledger should expose bounded limitations, not hide them")

    scorecard_rows = read_csv(ROOT / "results" / "tables" / "v3_object_centric_scorecard.csv")
    if len(scorecard_rows) < 10:
        fail(problems, "v3 scorecard is too small")
    scorecard_claims = {row["claim_id"] for row in scorecard_rows}
    if not {"C1", "C2", "C3", "C4"}.issubset(scorecard_claims):
        fail(problems, "v3 scorecard does not cover C1-C4")

    claims = json.loads((ROOT / "results" / "claims_status.json").read_text(encoding="utf-8"))
    claim_status = {claim["id"]: claim["status"] for claim in claims["claims"]}
    for claim_id in ["C1", "C2", "C4"]:
        if claim_status.get(claim_id) != "strongly_supported":
            fail(problems, f"{claim_id} is not strongly supported")
    if claim_status.get("C3") not in {"partial", "strongly_supported"}:
        fail(problems, "C3 is neither partial nor strongly supported")
    for claim_id in ["C5", "C6", "C7"]:
        if claim_status.get(claim_id) != "unsupported":
            fail(problems, f"{claim_id} boundary claim is not unsupported")
    if claims.get("forbidden_supported_overclaims") or claims.get("paper_text_overclaims"):
        fail(problems, "base claim audit reports overclaims")

    audit_text(problems)

    payload = {
        "passes": not problems,
        "problems": problems,
        "pages": pages,
        "sha256": repo_sha,
        "desktop_pdf": str(DESKTOP_FINAL),
        "repo_final_pdf": str(REPO_FINAL),
        "attack_rounds": len(attack_rows),
    }
    print(json.dumps(payload, indent=2))
    (ROOT / "results" / "v3_object_centric_final_audit.json").write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
