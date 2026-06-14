# V3 Execution Plan: Object-Centric Binding Tail Audit

## Current Claim

This paper claims that top-score selection over object-centric candidate futures can amplify object binding failures: selected object score can rise while selected real utility falls because the selected future is bound to the wrong target object. The strongest positive claims are:

- C1: exact finite tie-aware selected-utility law on finite candidate populations.
- C2: controlled selected-tail object-binding failure with negative controls and stress variants.
- C3: tiered repair evidence, with deployable no-leak evidence separated from support-covered diagnostics and oracle upper bounds.
- C4: CPU NumPy semi-learned object-centric evidence for property, identity-alignment, reward, learned selection, and learned repair-policy transfer.

Unsupported boundary claims stay explicit: no real-robot validation, no broad external benchmark superiority, and no universal repair or guaranteed recovery.

## Gaps in the 7-Page Baseline

- The baseline manuscript exposed only a small fraction of the existing result suite.
- It did not visibly separate all no-leak, support-covered, and oracle rows in submission-facing prose.
- It did not include enough stress panels, pilot-label evidence, noisy-probe/probe-cost checks, learned selection transfer, learned repair-policy transfer, or reviewer attack responses.
- It was too short for submission readiness and could look like a generic candidate-budget wrapper if read beside other papers.

## Target Experiments and Evidence

Use cached audited artifacts rather than rerunning the heavy full suite unless a true artifact gap appears. Required evidence families:

- exact-law validation from `exact_law_validation.csv`;
- raw selected-tail failure from `main_metrics.csv`;
- good-scene negative controls from `negative_control.csv`;
- dense and extreme object-count stress from `ood_metrics.csv` and `extreme_object_count_metrics.csv`;
- domain randomization, counterfactual target, target-identity sweep, and synthetic benchmark-style suite;
- repair comparison, observable repair, repair ablation, nested final-test repair robustness, and calibration diagnostics;
- deployment-gate policy, pilot calibration, pilot-budget sensitivity, leave-one-failure calibration, noisy probes, and probe costs;
- learned object model, learned ablations, learned domain shift, learned selection transfer, learned repair-policy transfer, and learned generalization diagnostics;
- bootstrap statistical audit and toy model-family proxy diagnostics.

## Baselines, Ablations, and Stress Tests

Baselines:
- raw high-budget selector;
- raw stop-early fallback;
- random selector;
- reward-only learned selector;
- toy latent-global, relational-slot, and diffusion-score proxy selectors;
- oracle upper bound.

Ablations:
- identity-only, property-only, probe-only, observable-only, and combined repair;
- learned no-mass and no-kinematic-pair feature ablations;
- pilot-label budget sweep;
- leave-one-failure-family-out calibration.

Stress tests:
- dense 6/8-object scenes;
- extreme 10/12-object scenes;
- occlusion, crossing, hidden-property, merge/split, and mixed corruptions;
- counterfactual target and six-target sweep;
- domain-randomized scenes;
- noisy diagnostic probes;
- probe-cost utility penalties;
- hidden-mode unidentifiable negative control.

## Figures and Tables

Generate v3 synthesis artifacts:

- `figure32_v3_evidence_scorecard.png`;
- `figure33_v3_repair_tiers.png`;
- `figure34_v3_stress_scope.png`;
- `figure35_v3_learned_transfer.png`;
- `figure36_v3_deployment_friction.png`;
- `figure37_v3_attack_coverage.png`;
- `v3_object_centric_scorecard.csv`;
- `v3_object_centric_attack_ledger.csv`;
- LaTeX versions of the v3 scorecard and 50-round self-attack ledger.

## Writing Expansion

The manuscript must be rewritten around object slots and binding rather than generic candidate-budget scaling. Required sections:

- abstract with exact scope and partial C3 language;
- object-centric introduction and contribution list;
- finite selected-utility law as audit machinery;
- scene/slot/target/failure-family method;
- repair tiers and leakage control;
- RQ-organized evidence sections;
- related work, limitations, reproducibility, conclusion;
- appendices for derivation, generator details, repair selectors, stress gallery, deployment frictions, learned artifact, statistical/proxy diagnostics, 50-round attack ledger, artifact inventory, and submission checklist.

## Page-Count Strategy

Minimum accepted PDF length is 25 pages. The length must come from real content:

- main text with complete method and evidence narrative;
- full stress and learned-evidence appendix figures;
- generated scorecard table and 50-round attack ledger;
- artifact inventory and reproducibility checklist.

## RAM-Light Execution Strategy

- Use `scripts/prepare_v3_evidence.py` to synthesize cached results from CSV/JSON files.
- Avoid rerunning `scripts/run_all.sh` unless the claim audit detects missing or stale core artifacts.
- Run validation sequentially: v3 evidence, LaTeX build, v3 audit, claim audit, tests.
- Prefer compact CSV/JSON summaries and generated plots over in-memory candidate arrays.
- Keep full canonical experiment suite available but not part of routine v3 rebuild.

## Final Acceptance Checklist

- PDF builds without fatal LaTeX errors and has at least 25 pages.
- Repo final PDF and Desktop final PDF are byte-identical by SHA-256.
- Desktop has `object centric-v3.pdf`; old `object centric-v2.pdf` is removed.
- `PAPER_SOURCE_MAP.md` maps `object centric-v3.pdf` to `C:\Users\wangz\object centric` and `Jason-Wang313/object-centric`.
- The v3 attack ledger has exactly 50 rounds.
- C1, C2, and C4 remain strongly supported; C3 remains either partial or stronger but is never inflated.
- No real-robot, broad benchmark superiority, or universal-repair overclaim appears in supported text.
- `python scripts/prepare_v3_evidence.py`, `bash scripts/build_iclr_paper.sh`, `python scripts/run_v3_claim_audit.py`, `bash scripts/run_claim_audit.sh`, `python -m compileall`, and `pytest` pass.
- Final commit is pushed to GitHub and remote SHA is verified.
