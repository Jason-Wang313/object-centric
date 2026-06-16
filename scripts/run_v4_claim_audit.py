"""Audit the v4 final object-centric paper, source map, and claim gates."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DESKTOP = Path.home() / "OneDrive" / "Desktop"
SOURCE_MAP = DESKTOP / "PAPER_SOURCE_MAP.md"
FINAL_NAME = "object centric-v4.pdf"
REPO_FINAL = ROOT / "paper" / "final" / FINAL_NAME
DESKTOP_FINAL = DESKTOP / FINAL_NAME
MANIFEST = ROOT / "paper" / "final" / "object_centric_v4_manifest.json"
OLD_DESKTOPS = [
    DESKTOP / "object centric-v3.pdf",
    DESKTOP / "object centric-v2.pdf",
]
MIN_PAGES = 25


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def pdf_pages(path: Path) -> int:
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
    text_path = ROOT / "build" / "v4_final_audit_text.txt"
    text_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["pdftotext", "-layout", str(path), str(text_path)], cwd=ROOT, check=True)
    return text_path.read_text(encoding="utf-8", errors="replace")


def check(rows: list[dict[str, Any]], name: str, ok: bool, evidence: Any) -> None:
    rows.append({"check": name, "status": "PASS" if ok else "FAIL", "evidence": evidence})


def main() -> int:
    subprocess.run([sys.executable, "experiments/v4_cached_evidence.py"], cwd=ROOT, check=True)
    summary = load_json(ROOT / "results" / "v4_cached_evidence_summary.json")
    claims = load_json(ROOT / "results" / "claims_status.json")
    manifest = load_json(MANIFEST) if MANIFEST.exists() else {}

    rows: list[dict[str, Any]] = []
    check(rows, "repo_final_pdf_exists", REPO_FINAL.exists() and REPO_FINAL.stat().st_size > 0, str(REPO_FINAL))
    check(rows, "desktop_final_pdf_exists", DESKTOP_FINAL.exists() and DESKTOP_FINAL.stat().st_size > 0, str(DESKTOP_FINAL))
    if REPO_FINAL.exists() and DESKTOP_FINAL.exists():
        repo_sha = sha256(REPO_FINAL)
        desktop_sha = sha256(DESKTOP_FINAL)
        check(rows, "repo_desktop_sha_match", repo_sha == desktop_sha, {"repo": repo_sha, "desktop": desktop_sha})
    else:
        repo_sha = ""
        desktop_sha = ""
        check(rows, "repo_desktop_sha_match", False, "missing final PDFs")

    pages = pdf_pages(REPO_FINAL) if REPO_FINAL.exists() else 0
    check(rows, "page_count_at_least_25", pages >= MIN_PAGES, pages)
    text = pdf_text(REPO_FINAL) if REPO_FINAL.exists() else ""
    compact = "".join(ch for ch in text.lower() if ch.isalnum())
    for marker in [
        "objectslotsunderselectionpressure",
        "protocolfreeze",
        "iclrstylerubric",
        "v4reviewerattackledger",
        "benchmarkstylesynthetictasksuite",
        "deployablenoleak",
        "supportcovered",
        "slotattention",
        "conformalprediction",
    ]:
        check(rows, f"pdf_marker_{marker}", marker in compact, marker)

    forbidden_exact = [
        "we validate on real robots",
        "we solve real robot planning",
        "we claim broad benchmark superiority",
        "achieves broad benchmark superiority",
        "is a universal repair",
        "guarantees recovery",
    ]
    lower_text = text.lower()
    hits = [phrase for phrase in forbidden_exact if phrase in lower_text]
    check(rows, "forbidden_positive_overclaims_absent", not hits, hits)

    check(rows, "v4_cached_only", summary.get("uses_cached_artifacts_only") is True, summary.get("uses_cached_artifacts_only"))
    check(rows, "v4_scorecard_rows", int(summary.get("submission_scorecard_rows", 0)) >= 12, summary.get("submission_scorecard_rows"))
    check(rows, "v4_attack_rounds_60_pass", summary.get("attack_rounds") == 60 and summary.get("attack_rounds_passed") == 60, {"rounds": summary.get("attack_rounds"), "passed": summary.get("attack_rounds_passed")})
    check(rows, "v4_protocol_gates_clean", summary.get("protocol_gates") == summary.get("protocol_gates_passed") == 12, {"passed": summary.get("protocol_gates_passed"), "total": summary.get("protocol_gates")})
    check(rows, "v4_rubric_axes_clean", summary.get("rubric_axes") == summary.get("rubric_axes_passed") == 7, {"passed": summary.get("rubric_axes_passed"), "total": summary.get("rubric_axes")})
    check(rows, "v4_artifact_checks", int(summary.get("artifact_checks", 0)) >= 100, summary.get("artifact_checks"))
    check(rows, "v4_citation_markers", int(summary.get("in_text_citation_markers", 0)) >= 10, summary.get("in_text_citation_markers"))

    status = {claim["id"]: claim["status"] for claim in claims["claims"]}
    check(rows, "core_claim_statuses", status.get("C1") == "strongly_supported" and status.get("C2") == "strongly_supported" and status.get("C4") == "strongly_supported" and status.get("C3") in {"partial", "strongly_supported"}, status)
    check(rows, "boundary_nonclaims", all(status.get(cid) == "unsupported" for cid in ["C5", "C6", "C7"]), status)
    check(rows, "base_claim_audit_clean", claims.get("passes_claim_audit") is True and not claims.get("forbidden_supported_overclaims") and not claims.get("paper_text_overclaims"), {"passes": claims.get("passes_claim_audit"), "forbidden": claims.get("forbidden_supported_overclaims"), "text": claims.get("paper_text_overclaims")})
    check(rows, "artifact_verification_clean", claims.get("artifact_verification", {}).get("passes") is True, claims.get("artifact_verification", {}))
    check(rows, "paper_claim_coverage_clean", claims.get("paper_claim_coverage", {}).get("passes") is True, claims.get("paper_claim_coverage", {}).get("problems", []))

    check(rows, "manifest_matches_pdf", manifest.get("sha256") == repo_sha and int(manifest.get("pages", 0)) == pages and manifest.get("version") == "v4", manifest)
    for old_desktop in OLD_DESKTOPS:
        check(rows, f"old_desktop_absent_{old_desktop.name}", not old_desktop.exists(), str(old_desktop))

    source_map_text = SOURCE_MAP.read_text(encoding="utf-8", errors="replace") if SOURCE_MAP.exists() else ""
    expected_row = f"| `{FINAL_NAME}` | `{ROOT}` | `Jason-Wang313/object-centric` |"
    stale_rows = [
        f"| `object centric-v3.pdf` | `{ROOT}` | `Jason-Wang313/object-centric` |",
        f"| `object centric-v2.pdf` | `{ROOT}` | `Jason-Wang313/object-centric` |",
    ]
    check(rows, "source_map_v4_row_present", expected_row in source_map_text, expected_row)
    check(rows, "source_map_stale_rows_absent", not any(row in source_map_text for row in stale_rows), stale_rows)

    failed = [row for row in rows if row["status"] == "FAIL"]
    audit = {
        "overall_status": "PASS" if not failed else "FAIL",
        "num_checks": len(rows),
        "num_pass": len(rows) - len(failed),
        "num_fail": len(failed),
        "failed_checks": failed,
        "pages": pages,
        "repo_sha256": repo_sha,
        "desktop_sha256": desktop_sha,
    }
    out = ROOT / "results" / "v4_claim_audit_summary.json"
    out.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(audit, indent=2, sort_keys=True))
    return 0 if not failed else 2


if __name__ == "__main__":
    raise SystemExit(main())
