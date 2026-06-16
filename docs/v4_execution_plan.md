# V4 Execution Plan: Object-Centric Binding Tail Audit

## Claim Identity

The paper is an object-slot binding audit, not a generic candidate-budget theorem paper. The finite selected-utility law is a measuring device. The contribution is the controlled object-centric population: target identity, slot binding, occlusion drift, merge/split failures, hidden properties, repair tiers, and learned object-slot diagnostics.

## Frozen Evidence Policy

Use the existing audited CSV/JSON artifacts as the canonical experiment record. The v4 synthesis regenerates cached evidence, protocol gates, rubric maps, reviewer attacks, figures, and LaTeX tables without rerunning the heavy full experiment suite.

## Required V4 Additions

- Add visible in-text citations for object-centric learning, relational dynamics, world-model planning, calibration, conformal prediction, and benchmark context.
- Add a v4 submission scorecard that separates raw failure, negative controls, stress panels, no-leak repair, support-covered repair, oracle rows, deployment frictions, learned transfer, and statistical audits.
- Add protocol-freeze gates: code, seeds, task families, metrics, baselines, stress conditions, thresholds, claim gates, citation coverage, reviewer loop, and final measurement-only reporting.
- Add ICLR-style rubric gates: novelty, empirical rigor, baselines, stress/negative controls, statistical caution, reproducibility, and scope control.
- Extend the harsh-reviewer ledger from 50 to 60 rounds.
- Do not claim real-robot validation, broad external-benchmark superiority, universal repair, or guaranteed recovery.

## Final Acceptance Checklist

- `python experiments/v4_cached_evidence.py` passes.
- `python scripts/build_v4_paper.py` produces `object centric-v4.pdf` in `paper/final/` and on the Desktop.
- `python scripts/run_v4_claim_audit.py` passes with matching repo/Desktop hashes.
- `bash scripts/run_claim_audit.sh`, `python -m pytest -q`, and `python -m compileall src experiments scripts tests -q` pass.
- The Desktop source map points `object centric-v4.pdf` to `C:\Users\wangz\object centric` and `Jason-Wang313/object-centric`.
- The final branch is pushed to GitHub and the remote SHA matches local `HEAD`.
